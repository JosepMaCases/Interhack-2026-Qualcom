import time
from arduino_bridge import bridge

while True:
    result = bridge.call("get_distance")
    distance_mm = int(result)

    if distance_mm >= 0:
        print(f"Distància: {distance_mm} mm")
    else:
        print("No detecta objecte")

    time.sleep(0.2)