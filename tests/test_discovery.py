import pytest
from server.server import parse_discovery_message


@pytest.mark.parametrize(
    "msg",
    [
        {"invalid": "json"},
        {
            "dev_cla": "temperature",
            "unit_of_meas": "°C",
            "stat_cla": "measurement",
            "name": "Temperature",
            "stat_t": "humidity-temperature/sensor/temperature/state",
            "avty_t": "humidity-temperature/status",
            "uniq_id": "ESPsensortemperature",
            "dev": {
                "ids": "ec94cb6cbcc8",
                "name": "humidity-temperature",
                "sw": "esphome v2022.12.3 Apr 13 2023, 15:17:14",
                "mdl": "esp32doit-devkit-v1",
                "mf": "espressif",
            },
        },
        {
            "dev_cla": "humidity",
            "unit_of_meas": "%",
            "stat_cla": "measurement",
            "name": "Humidity",
            "stat_t": "humidity-temperature/sensor/humidity/state",
            "avty_t": "humidity-temperature/status",
            "uniq_id": "ESPsensorhumidity",
            "dev": {
                "ids": "ec94cb6cbcc8",
                "name": "humidity-temperature",
                "sw": "esphome v2022.12.3 Apr 13 2023, 15:17:14",
                "mdl": "esp32doit-devkit-v1",
                "mf": "espressif",
            },
        },
        {
            "min": 5,
            "max": 120,
            "step": 1,
            "unit_of_meas": "Seconds",
            "name": "Backlight on time (seconds)",
            "stat_t": "humidity-temperature/number/backlight_on_time_seconds/state",
            "cmd_t": "humidity-temperature/number/backlight_on_time_seconds/command",
            "avty_t": "humidity-temperature/status",
            "uniq_id": "ESPnumberbacklight_on_time_seconds",
            "dev": {
                "ids": "ec94cb6cbcc8",
                "name": "humidity-temperature",
                "sw": "esphome v2022.12.3 Apr 13 2023, 15:17:14",
                "mdl": "esp32doit-devkit-v1",
                "mf": "espressif",
            },
        },
        {
            "min": 0,
            "max": 1,
            "step": 0.01,
            "name": "Backlight Brightness",
            "stat_t": "humidity-temperature/number/backlight_brightness/state",
            "cmd_t": "humidity-temperature/number/backlight_brightness/command",
            "avty_t": "humidity-temperature/status",
            "uniq_id": "ESPnumberbacklight_brightness",
            "dev": {
                "ids": "ec94cb6cbcc8",
                "name": "humidity-temperature",
                "sw": "esphome v2022.12.3 Apr 13 2023, 15:17:14",
                "mdl": "esp32doit-devkit-v1",
                "mf": "espressif",
            },
        },
        {
            "schema": "json",
            "clrm": True,
            "supported_color_modes": ["onoff"],
            "name": "Status",
            "stat_t": "humidity-temperature/light/status/state",
            "cmd_t": "humidity-temperature/light/status/command",
            "avty_t": "humidity-temperature/status",
            "uniq_id": "ESPlightstatus",
            "dev": {
                "ids": "ec94cb6cbcc8",
                "name": "humidity-temperature",
                "sw": "esphome v2022.12.3 Apr 13 2023, 15:17:14",
                "mdl": "esp32doit-devkit-v1",
                "mf": "espressif",
            },
        },
        {
            "name": "Button",
            "stat_t": "humidity-temperature/binary_sensor/button/state",
            "avty_t": "humidity-temperature/status",
            "uniq_id": "ESPbinary_sensorbutton",
            "dev": {
                "ids": "ec94cb6cbcc8",
                "name": "humidity-temperature",
                "sw": "esphome v2022.12.3 Apr 13 2023, 15:17:14",
                "mdl": "esp32doit-devkit-v1",
                "mf": "espressif",
            },
        },
    ],
)
def test_parse_discovey(msg, data_regression):
    parsed = parse_discovery_message(msg)
    data_regression.check(parsed.dict() if hasattr(parsed, "dict") else parsed)
