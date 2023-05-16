#ifndef TACTIDUINO_SERVO_H
#define TACTIDUINO_SERVO_H

#include <Arduino.h>
#include "Software_I2C_Adafruit_PWMServoDriver.h"

class Servo {
private:
    Software_I2C_Adafruit_PWMServoDriver &pwm;
    int address;
    int impulsion_min = 150;
    int impulsion_max = 600;
    int angle_min = 0;
    int angle_max = 180;
    long angle = 0;
    long targetAngle = 0;

public:
    Servo(Software_I2C_Adafruit_PWMServoDriver &pwm, int address);

    Servo(Software_I2C_Adafruit_PWMServoDriver &pwm, int address, int angle_min, int angle_max);

    void set_angle(long angle);

    void tick();
};

#endif //TACTIDUINO_SERVO_H
