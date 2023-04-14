from datetime import datetime

from pydantic import BaseModel, ValidationError, validator


class ValueBase(BaseModel):
    value: bool | float | str
    timestamp: datetime

    @validator("value")
    def validate_value(cls, v):
        match v:
            case "ON":
                return True
            case "OFF":
                return False
            case float(v):
                return v
            case str(v):
                try:
                    return float(v)
                except ValueError:
                    return v


class ValueCreate(ValueBase):
    pass


class Value(ValueBase):
    class Config:
        orm_mode = True


class SensorBase(BaseModel):
    name: str
    uniq_id: str
    state_topic: str
    unit_of_measurement: str | None = None
    device_class: str | None = None


class Sensor(SensorBase):
    # values: list[Value] = []

    class Config:
        orm_mode = True


class SensorCreate(SensorBase):
    pass
