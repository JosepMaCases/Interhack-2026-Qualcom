from datetime import datetime, UTC

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI

logger = Logger("helmet-api")

ui = WebUI(cors_origins="")

latest_sensors = {
    "distance_mm": None,
    "temperature_c": None,
    "humidity_percent": None,
    "movement": {
        "x": None,
        "y": None,
        "z": None,
    },
    "status": {
        "moving": False,
        "zone": "NO_DISTANCE",
        "zone_code": 1,
    },
    "updated_at": None,
}

ZONES = {
    0: "STOPPED",
    1: "NO_DISTANCE",
    2: "FAR",
    3: "WARNING",
    4: "DANGER",
    5: "CRITICAL",
}


def now_iso():
    return datetime.now(UTC).isoformat()


def update_timestamp():
    latest_sensors["updated_at"] = now_iso()


def record_distance(distance_mm: float):
    latest_sensors["distance_mm"] = int(distance_mm)
    update_timestamp()
    print(f"Distancia: {int(distance_mm)} mm")


def record_thermo(temperature: float, humidity: float):
    latest_sensors["temperature_c"] = round(float(temperature), 1)
    latest_sensors["humidity_percent"] = round(float(humidity), 1)
    update_timestamp()
    print(f"Temperatura: {temperature:.1f} C | Humitat: {humidity:.1f} %")


def record_movement(x: float, y: float, z: float):
    latest_sensors["movement"] = {
        "x": round(float(x), 3),
        "y": round(float(y), 3),
        "z": round(float(z), 3),
    }
    update_timestamp()
    print(f"Moviment: x={x:.3f} y={y:.3f} z={z:.3f}")


def record_status(moving: int, distance_mm: int, zone_code: int):
    zone_code = int(zone_code)
    movement_state = "moving" if int(moving) == 1 else "stopped"
    zone = ZONES.get(zone_code, "UNKNOWN")

    latest_sensors["distance_mm"] = int(distance_mm)
    latest_sensors["status"] = {
        "moving": int(moving) == 1,
        "zone": zone,
        "zone_code": zone_code,
    }
    update_timestamp()
    print(f"Estat: {movement_state} | Distancia: {distance_mm} mm | Zona: {zone}")


def get_sensors():
    return latest_sensors


try:
    Bridge.provide("record_distance", record_distance)
    Bridge.provide("record_thermo", record_thermo)
    Bridge.provide("record_movement", record_movement)
    Bridge.provide("record_status", record_status)

except RuntimeError:
    logger.debug("Bridge handlers already registered")

ui.expose_api("GET", "/sensors", get_sensors)

App.run()
