from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utc import UtcDateTime

from .database import Base


class Sensor(Base):
    __tablename__ = "sensors"
    name = Column(String, index=True)
    uniq_id = Column(String, index=True, primary_key=True)
    state_topic = Column(String, index=True)
    unit_of_measurement = Column(String, index=True)
    device_class = Column(String, index=True)
    values = relationship("Value", back_populates="sensor")


class Value(Base):
    """A value."""

    __tablename__ = "values"
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, index=True)
    value = Column(String, index=True)
    timestamp = Column(UtcDateTime, index=True)
    sensor_id = Column(String, ForeignKey("sensors.uniq_id"))
    sensor = relationship("Sensor", back_populates="values")
