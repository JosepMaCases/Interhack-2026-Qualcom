from arduino.app_utils import *

logger = Logger("distance-app")

def record_distance(distance_mm: float):

    print(f"Distància: {distance_mm} mm")

try:
    Bridge.provide("record_distance", record_distance)

except RuntimeError:
    logger.debug("'record_distance' already registered")

App.run()