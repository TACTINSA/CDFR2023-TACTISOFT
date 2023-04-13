#include <Arduino.h>
#include "sharp.h"

Sharp sharps[] = {
        Sharp(A0),
        Sharp(A1),
        Sharp(A2),
        Sharp(A3),
        Sharp(A4),
        Sharp(A5),
        Sharp(A6),
        Sharp(A7),
};

int counter = 0;

void setup() {
    Serial.begin (9600);  // démarre le port série
}

void loop() {
    for (Sharp & sharp : sharps) {
        sharp.tick();
    }

    if (counter > 100) {
        for (Sharp & sharp : sharps) {
            Serial.print((int) sharp.getDistance());
            Serial.print(" ");
        }
        Serial.println();
        counter = 0;
    }
    counter++;

    delay(10);
}