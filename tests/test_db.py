from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory

import pytest
from fastapi.testclient import TestClient
from server import models
from server.database import Base
from server.schemas import SensorCreate
from server.server import app, create_sensor, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def local_tmp_path():
    i = 0
    while (p := Path(f"./tmp{i}")).exists():
        i += 1
    p.mkdir()
    yield p
    rmtree(p)


@pytest.fixture()
def local_session(local_tmp_path):
    return new_session(local_tmp_path)


def new_session(tmp_path):
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{tmp_path.relative_to('.')}/test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal


@pytest.fixture
def tmp_db(local_session):
    db = local_session()
    try:
        yield db
    finally:
        db.close()


# def override_get_db():
#     db = None
#     try:
#         db = new_session("/./")()
#         yield db
#     finally:
#         if db:
#             db.close()


# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)


def test_create_retrieve_sensor(tmp_db):
    sensor = SensorCreate(name="sensor1", uniq_id="id_1", state_topic="sensors/id_1")
    resp = create_sensor(sensor, tmp_db)
    assert isinstance(resp, models.Sensor)


def test_create_duplicate_sensor(tmp_db):
    sensor = SensorCreate(name="sensor1", uniq_id="id_1", state_topic="sensors/id_1")
    resp = create_sensor(sensor, tmp_db)
    assert isinstance(resp, models.Sensor)
    resp = create_sensor(sensor, tmp_db)
    assert resp is None
