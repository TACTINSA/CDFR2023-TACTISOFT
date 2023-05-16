#ifndef TACTIDUINO_SHARP_H
#define TACTIDUINO_SHARP_H

#include <Arduino.h>

#define SHARP_SAMPLES 10

class Sharp {
private:
    int pin;
    int values[SHARP_SAMPLES] = {};
    int index = 0;
    int detection_distance = INT16_MAX;
    bool is_bellow = false;
    bool is_acknowledged = false;

public:
    explicit Sharp(int pin, int detection_distance);

    void tick();

    double getDistance() const;

    bool isBellow() const;
};

#endif //TACTIDUINO_SHARP_H
