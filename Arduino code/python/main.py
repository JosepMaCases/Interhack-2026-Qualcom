from arduino.app_utils import *

logger = Logger("distance-app")


def record_distance(distance_mm: float):
    print(f"Distancia: {distance_mm} mm")


def record_thermo(temperature: float, humidity: float):
    print(f"Temperatura: {temperature} C | Humitat: {humidity} %")


def record_movement(x: float, y: float, z: float):
    print(f"Moviment: x={x} y={y} z={z}")


try:
    Bridge.provide("record_distance", record_distance)
    Bridge.provide("record_thermo", record_thermo)
    Bridge.provide("record_movement", record_movement)

except RuntimeError:
    logger.debug("Bridge handlers already registered")

App.run()
