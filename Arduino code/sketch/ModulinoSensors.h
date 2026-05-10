#ifndef MODULINO_SENSORS_H
#define MODULINO_SENSORS_H

#include <Arduino.h>
#include <Arduino_Modulino.h>
#include <Arduino_RouterBridge.h>

class ModulinoSensors {
public:
  void begin() {
    Bridge.begin();
    Modulino.begin(Wire1);

    distance.begin();
    buzzer.begin();
    vibro.begin();
    thermo.begin();
    pixels.begin();
    movement.begin();
  }

  bool distanceAvailable() {
    return distance.available();
  }

  int distanceMillimeters() {
    return distance.get();
  }

  void notifyDistance(int distanceMm) {
    Bridge.notify("record_distance", distanceMm);
  }

  void playTone(int frequency, int durationMs) {
    buzzer.tone(frequency, durationMs);
  }

  void stopTone(int durationMs) {
    buzzer.tone(0, durationMs);
  }

  void vibrate(size_t durationMs) {
    vibro.on(durationMs);
  }

  void vibrate(size_t durationMs, VibroPowerLevel powerLevel) {
    vibro.on(durationMs, powerLevel);
  }

  void stopVibration() {
    vibro.off();
  }

  float temperatureCelsius() {
    return thermo.getTemperature();
  }

  float humidityPercent() {
    return thermo.getHumidity();
  }

  void notifyThermo() {
    Bridge.notify("record_thermo", temperatureCelsius(), humidityPercent());
  }

  void clearPixels() {
    pixels.clear();
  }

  void clearPixel(int pixel) {
    pixels.clear(pixel);
  }

  void setPixel(int pixel, ModulinoColor color, int brightness) {
    pixels.set(pixel, color, brightness);
  }

  void setPixel(int pixel, int red, int green, int blue, int brightness) {
    pixels.set(pixel, red, green, blue, brightness);
  }

  void setAllPixels(ModulinoColor color, int brightness) {
    for (int pixel = 0; pixel < 8; pixel++) {
      pixels.set(pixel, color, brightness);
    }
  }

  void setPixelBar(int count, ModulinoColor color, int brightness) {
    pixels.clear();

    for (int pixel = 0; pixel < count && pixel < 8; pixel++) {
      pixels.set(pixel, color, brightness);
    }
  }

  void showPixels() {
    pixels.show();
  }

  bool updateMovement() {
    return movement.update();
  }

  float movementX() {
    return movement.getX();
  }

  float movementY() {
    return movement.getY();
  }

  float movementZ() {
    return movement.getZ();
  }

  void notifyMovement() {
    Bridge.notify("record_movement", movementX(), movementY(), movementZ());
  }

  void notifyStatus(bool moving, int distanceMm, int zone) {
    Bridge.notify("record_status", moving ? 1 : 0, distanceMm, zone);
  }

private:
  ModulinoDistance distance;
  ModulinoBuzzer buzzer;
  ModulinoVibro vibro;
  ModulinoThermo thermo;
  ModulinoPixels pixels;
  ModulinoMovement movement;
};

#endif
