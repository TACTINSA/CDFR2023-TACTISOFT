#include "sharp.h"

Sharp::Sharp(int pin, int detection_distance) {
    this->pin = pin;
    this->detection_distance = detection_distance;
    for (int &value: values) {
        value = analogRead(pin);
    }
}

void Sharp::tick() {
    values[index] = analogRead(pin);
    index++;
    if (index >= SHARP_SAMPLES) {
        index = 0;
    }
}

bool Sharp::isBellow() const {
    return this->getDistance() < detection_distance;
}

double Sharp::getDistance() const {
    float sum = 0;
    for (int value: values) {
        sum += value;
    }
    double average = sum / SHARP_SAMPLES;
    double volt = average * 0.0048828125f;
    return 28 * pow(volt, -1);
}
