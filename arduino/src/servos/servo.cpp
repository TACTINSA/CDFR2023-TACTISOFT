#include "servo.h"

Servo::Servo(Software_I2C_Adafruit_PWMServoDriver &pwm, int address) : pwm(pwm), address(address) {}

Servo::Servo(Software_I2C_Adafruit_PWMServoDriver &pwm, int address, int impulsion_min, int impulsion_max) : pwm(pwm), address(address), impulsion_min(impulsion_min), impulsion_max(impulsion_max) {}

void Servo::set_angle(long target) {
    this->targetAngle = target;
}

void Servo::tick() {
    if (targetAngle == angle)
        return;

    if (targetAngle > angle) {
        angle++;
    } else {
        angle--;
    }

    long impulsion = map(angle, 0, 270, impulsion_min, impulsion_max);
    pwm.setPWM(address, 0, impulsion);
}