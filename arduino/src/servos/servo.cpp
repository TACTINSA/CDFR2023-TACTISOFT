#include "servo.h"

Servo::Servo(Software_I2C_Adafruit_PWMServoDriver &pwm, int address) : pwm(pwm), address(address) {}

Servo::Servo(Software_I2C_Adafruit_PWMServoDriver &pwm, int address, int angle_min, int angle_max) : pwm(pwm),
                                                                                                     address(address),
                                                                                                     angle_min(angle_min),
                                                                                                     angle_max(angle_max) {}

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

    long impulsion = map(angle, angle_min, angle_max, impulsion_min, impulsion_max);
    pwm.setPWM(address, 0, impulsion);
}