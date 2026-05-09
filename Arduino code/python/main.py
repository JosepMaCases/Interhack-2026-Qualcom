from arduino.app_utils import *

logger = Logger("distance-app")


def record_distance(distance_mm: float):
    print(f"Distancia: {distance_mm} mm")


def record_thermo(temperature: float, humidity: float):
    print(f"Temperatura: {temperature:.1f} C | Humitat: {humidity:.1f} %")


def record_movement(x: float, y: float, z: float):
    print(f"Moviment: x={x:.3f} y={y:.3f} z={z:.3f}")


def record_status(moving: int, distance_mm: int, zone_code: int):
    zones = {
        0: "STOPPED",
        1: "NO_DISTANCE",
        2: "FAR",
        3: "WARNING",
        4: "DANGER",
        5: "CRITICAL",
    }
    movement_state = "moving" if int(moving) == 1 else "stopped"
    zone = zones.get(int(zone_code), "UNKNOWN")
    print(f"Estat: {movement_state} | Distancia: {distance_mm} mm | Zona: {zone}")


try:
    Bridge.provide("record_distance", record_distance)
    Bridge.provide("record_thermo", record_thermo)
    Bridge.provide("record_movement", record_movement)
    Bridge.provide("record_status", record_status)

except RuntimeError:
    logger.debug("Bridge handlers already registered")

App.run()
