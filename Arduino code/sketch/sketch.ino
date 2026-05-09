#include <Arduino_Modulino.h>
#include <Arduino_RouterBridge.h>

ModulinoDistance distance;

unsigned long previousMillis = 0;
const long interval = 100; // cada 100ms

void setup() {
  Bridge.begin();

  Modulino.begin(Wire1);

  while (!distance.begin()) {
    delay(1000);
  }
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (distance.available()) {
      int distance_mm = distance.get();

      Bridge.notify("record_distance", distance_mm);
    }
  }
}