#include "ModulinoSensors.h"

ModulinoSensors sensors;

const unsigned long SENSOR_INTERVAL_MS = 1000;
unsigned long lastSensorReadMs = 0;

void setup() {
  sensors.begin();

  sensors.clearPixels();
  sensors.showPixels();
}

void loop() {
  unsigned long now = millis();
  if (now - lastSensorReadMs < SENSOR_INTERVAL_MS) {
    return;
  }

  lastSensorReadMs = now;

  if (sensors.distanceAvailable()) {
    int distanceMm = sensors.distanceMillimeters();
    sensors.notifyDistance(distanceMm);

    if (distanceMm < 100) {
      sensors.setAllPixels(RED, 10);
      sensors.showPixels();
      sensors.playTone(440, 250);
      sensors.vibrate(100);
    } else {
      sensors.clearPixels();
      sensors.showPixels();
      sensors.stopTone(100);
      sensors.stopVibration();
    }
  }

  sensors.notifyThermo();

  if (sensors.updateMovement()) {
    sensors.notifyMovement();
  }
}
