from contextlib import contextmanager
from datetime import datetime, timezone
from json import loads

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas, secrets
from .database import SessionLocal, engine

app = FastAPI()

mqtt_config = MQTTConfig(**secrets.mqtt_config)
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

sensor_topics: dict[str, str] = {}

origins = ["*"]  # TODO limit when deployed

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_context = contextmanager(get_db)


def parse_discovery_message(msg: dict) -> schemas.SensorCreate | None:
    try:
        return schemas.SensorCreate(
            name=msg.get("name", None),
            uniq_id=msg.get("unique_id", msg.get("uniq_id", None)),
            state_topic=msg.get("state_topic", msg.get("stat_t", None)),
            unit_of_measurement=msg.get(
                "unit_of_measurement", msg.get("unit_of_meas", None)
            ),
            device_class=msg.get("device_class", msg.get("dev_cla", None)),
        )
    except ValidationError:
        return None


def create_sensor(sensor: schemas.SensorCreate, db: Session) -> models.Sensor | None:
    db_sensor = models.Sensor(**sensor.dict())
    try:
        db.add(db_sensor)
        db.commit()
        db.refresh(db_sensor)
        return db_sensor
    except IntegrityError:
        return None


@mqtt.subscribe("homeassistant/sensor/#")
async def msg(_client, _topic, payload, _qos, _properties):
    parsed = parse_discovery_message(loads(payload.decode()))
    if parsed:
        topic = parsed.state_topic
        mqtt.client.subscribe(topic)
        sensor_topics[topic] = parsed.uniq_id
        with db_context() as db:
            create_sensor(parsed, db)


def persist(sensor_id: str, value: str, db: Session):
    count = (
        db.query(
            func.max(models.Value.count).filter(models.Value.sensor_id == sensor_id)
        ).scalar()
        or 0
    )
    db_value = models.Value(
        sensor_id=sensor_id,
        value=value,
        timestamp=datetime.now(timezone.utc),
        count=count + 1,
    )
    db.add(db_value)
    db.commit()
    db.refresh(db_value)
    return db_value


@mqtt.on_message()
async def message(client, topic, payload, _qos, _properties):
    if sensor_id := sensor_topics.get(topic, None):
        with db_context() as db:
            persist(sensor_id, payload.decode(), db)


@app.get("/sensor")
async def get_sensor(uniq_id: str, db: Session = Depends(get_db)):
    return db.query(models.Sensor).filter(models.Sensor.uniq_id == uniq_id).first()


@app.get("/sensors", response_model=list[schemas.Sensor])
async def get_sensors(db: Session = Depends(get_db)):
    return db.query(models.Sensor).all()


@app.get("/values", response_model=list[schemas.Value] | None)
def get_values(
    sensor_id: str,
    start: datetime,
    end: datetime,
    n: int = 100,
    db: Session = Depends(get_db),
):
    if not start.tzinfo:
        start = start.replace(tzinfo=timezone.utc)
    if not end.tzinfo:
        end = end.replace(tzinfo=timezone.utc)
    return (
        (
            db.query(models.Value)
            .filter(models.Value.sensor_id == sensor_id)
            .filter(models.Value.timestamp < end)
            .filter(models.Value.timestamp > start)
        )
        .limit(n)
        .all()
    )


@app.get("/decimated-values", response_model=list[schemas.Value])
def get_decimated_values(
    sensor_id: str,
    start: datetime,
    end: datetime,
    n: int = 100,
    db: Session = Depends(get_db),
):
    available = (
        db.query(models.Value).filter(models.Value.sensor_id == sensor_id).count()
    )
    if n > available:
        n = available
    return (
        db.query(models.Value)
        .filter(models.Value.sensor_id == sensor_id)
        .filter(models.Value.count % (available // n) == 0)
        .filter(models.Value.timestamp < end)
        .filter(models.Value.timestamp > start)
    ).all()[-n:]
