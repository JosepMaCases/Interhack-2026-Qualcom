#include <math.h>

#include "ModulinoSensors.h"

enum ProximityZone {
  ZONE_STOPPED,
  ZONE_NO_DISTANCE,
  ZONE_FAR,
  ZONE_WARNING,
  ZONE_DANGER,
  ZONE_CRITICAL
};

ModulinoSensors sensors;
ModulinoColor yellowColor(100, 100, 0);

const unsigned long SENSOR_INTERVAL_MS = 100;
const unsigned long STATUS_INTERVAL_MS = 1000;
const unsigned long STOPPED_AFTER_MS = 2000;

const float MOVEMENT_DELTA_THRESHOLD = 0.08;
const int MOVEMENT_CONFIRM_SAMPLES = 3;

const int FAR_DISTANCE_MM = 800;
const int WARNING_DISTANCE_MM = 300;
const int CRITICAL_DISTANCE_MM = 120;

const int PIXEL_BRIGHTNESS = 10;
const int BEEP_FREQUENCY = 440;
const int BEEP_DURATION_MS = 80;
const int STOP_TONE_DURATION_MS = 100;

unsigned long lastSensorReadMs = 0;
unsigned long lastStatusMs = 0;
unsigned long lastMovementMs = 0;
unsigned long lastBeepMs = 0;

float lastX = 0;
float lastY = 0;
float lastZ = 0;
bool hasLastMovementSample = false;
bool isMoving = false;
int movementSampleCount = 0;

int latestDistanceMm = -1;
ProximityZone currentZone = ZONE_NO_DISTANCE;
bool alertsAreStopped = false;

void readMovement(unsigned long now);
void readDistance();
void updateProximityAlerts(unsigned long now);
ProximityZone getProximityZone(int distanceMm);
void beepEvery(unsigned long now, unsigned long intervalMs);
void beepAndVibrateEvery(unsigned long now, unsigned long intervalMs);
void updateBuzzer(unsigned long now);
void stopAlerts();
void notifyReadings(unsigned long now);

void setup() {
  sensors.begin();
  stopAlerts();
}

void loop() {
  unsigned long now = millis();

  if (now - lastSensorReadMs < SENSOR_INTERVAL_MS) {
    updateBuzzer(now);
    return;
  }

  lastSensorReadMs = now;

  readMovement(now);
  readDistance();
  updateProximityAlerts(now);
  notifyReadings(now);
}

void readMovement(unsigned long now) {
  if (!sensors.updateMovement()) {
    return;
  }

  float x = sensors.movementX();
  float y = sensors.movementY();
  float z = sensors.movementZ();

  if (hasLastMovementSample) {
    float delta = fabs(x - lastX) + fabs(y - lastY) + fabs(z - lastZ);

    if (delta > MOVEMENT_DELTA_THRESHOLD) {
      movementSampleCount++;
      lastMovementMs = now;
    } else if (movementSampleCount > 0) {
      movementSampleCount--;
    }

    if (movementSampleCount >= MOVEMENT_CONFIRM_SAMPLES) {
      isMoving = true;
      movementSampleCount = MOVEMENT_CONFIRM_SAMPLES;
    }
  } else {
    hasLastMovementSample = true;
    lastMovementMs = now;
  }

  if (isMoving && now - lastMovementMs >= STOPPED_AFTER_MS) {
    isMoving = false;
    movementSampleCount = 0;
  }

  lastX = x;
  lastY = y;
  lastZ = z;
}

void readDistance() {
  if (sensors.distanceAvailable()) {
    latestDistanceMm = sensors.distanceMillimeters();
  }
}

void updateProximityAlerts(unsigned long now) {
  if (!isMoving) {
    currentZone = ZONE_STOPPED;
    stopAlerts();
    return;
  }

  currentZone = getProximityZone(latestDistanceMm);

  switch (currentZone) {
    case ZONE_FAR:
      sensors.setPixelBar(2, GREEN, PIXEL_BRIGHTNESS);
      sensors.showPixels();
      alertsAreStopped = false;
      sensors.stopTone(STOP_TONE_DURATION_MS);
      sensors.stopVibration();
      break;

    case ZONE_WARNING:
      sensors.setPixelBar(5, yellowColor, PIXEL_BRIGHTNESS);
      sensors.showPixels();
      alertsAreStopped = false;
      sensors.stopVibration();
      beepEvery(now, 700);
      break;

    case ZONE_DANGER:
      sensors.setPixelBar(8, RED, PIXEL_BRIGHTNESS);
      sensors.showPixels();
      alertsAreStopped = false;
      sensors.stopVibration();
      beepEvery(now, 250);
      break;

    case ZONE_CRITICAL:
      sensors.setPixelBar(8, RED, PIXEL_BRIGHTNESS);
      sensors.showPixels();
      alertsAreStopped = false;
      beepAndVibrateEvery(now, 120);
      break;

    case ZONE_NO_DISTANCE:
    case ZONE_STOPPED:
    default:
      stopAlerts();
      break;
  }
}

ProximityZone getProximityZone(int distanceMm) {
  if (distanceMm < 0) {
    return ZONE_NO_DISTANCE;
  }

  if (distanceMm < CRITICAL_DISTANCE_MM) {
    return ZONE_CRITICAL;
  }

  if (distanceMm < WARNING_DISTANCE_MM) {
    return ZONE_DANGER;
  }

  if (distanceMm < FAR_DISTANCE_MM) {
    return ZONE_WARNING;
  }

  return ZONE_FAR;
}

void beepEvery(unsigned long now, unsigned long intervalMs) {
  if (now - lastBeepMs >= intervalMs) {
    lastBeepMs = now;
    sensors.playTone(BEEP_FREQUENCY, BEEP_DURATION_MS);
  }
}

void beepAndVibrateEvery(unsigned long now, unsigned long intervalMs) {
  if (now - lastBeepMs >= intervalMs) {
    lastBeepMs = now;
    sensors.playTone(BEEP_FREQUENCY, BEEP_DURATION_MS);
    sensors.vibrate(100);
  }
}

void updateBuzzer(unsigned long now) {
  if (!isMoving || currentZone == ZONE_FAR || currentZone == ZONE_NO_DISTANCE || currentZone == ZONE_STOPPED) {
    return;
  }

  if (currentZone == ZONE_WARNING) {
    beepEvery(now, 700);
  } else if (currentZone == ZONE_DANGER) {
    beepEvery(now, 250);
  } else if (currentZone == ZONE_CRITICAL) {
    beepAndVibrateEvery(now, 120);
  }
}

void stopAlerts() {
  if (alertsAreStopped) {
    return;
  }

  sensors.clearPixels();
  sensors.showPixels();
  sensors.stopTone(STOP_TONE_DURATION_MS);
  sensors.stopVibration();
  alertsAreStopped = true;
}

void notifyReadings(unsigned long now) {
  if (now - lastStatusMs < STATUS_INTERVAL_MS) {
    return;
  }

  lastStatusMs = now;

  sensors.notifyStatus(isMoving, latestDistanceMm, (int)currentZone);
  sensors.notifyThermo();
  sensors.notifyMovement();

  if (latestDistanceMm >= 0) {
    sensors.notifyDistance(latestDistanceMm);
  }
}
