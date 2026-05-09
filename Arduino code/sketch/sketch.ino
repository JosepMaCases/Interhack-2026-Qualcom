#include <Arduino_RouterBridge.h>
#include <Modulino.h>

Bridge Bridge;

ModulinoDistance distance;

int get_distance() {
  if (distance.available()) {
    return distance.get();   // retorna mm
  }
  return -1; // cap objecte o lectura no disponible
}

void setup() {
  Modulino.begin();
  distance.begin();

  Bridge.begin();
  Bridge.provide("get_distance", get_distance);
}

void loop() {
  Bridge.update();
}