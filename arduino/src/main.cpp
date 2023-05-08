#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#include <servos/Software_I2C_Adafruit_PWMServoDriver.h>
#include "sharps/sharp.h"
#include "servos/servo.h"


#define COMMAND_PREFIX "R2+"
#define DISTANCE_DETECTION 30

#define PIN_TIRETTE 2
#define PIN_LED 6

#define NB_LEDS 20

uint32_t red = Adafruit_NeoPixel::Color(255, 0, 0);
Adafruit_NeoPixel pixels(NB_LEDS, PIN_LED, NEO_GRB);

Sharp sharps[] = {
        Sharp(A0, DISTANCE_DETECTION),
        Sharp(A1, DISTANCE_DETECTION),
        Sharp(A2, DISTANCE_DETECTION),
        Sharp(A3, DISTANCE_DETECTION),
        Sharp(A4, DISTANCE_DETECTION),
        Sharp(A5, DISTANCE_DETECTION),
        Sharp(A6, DISTANCE_DETECTION),
        Sharp(A7, DISTANCE_DETECTION),
};

Software_I2C_Adafruit_PWMServoDriver pwm = Software_I2C_Adafruit_PWMServoDriver(12, 11);
Servo servos[] = {
        Servo(pwm, 0, 0, 270),
        Servo(pwm, 1, 0, 270),
        Servo(pwm, 2)
};

enum check_direction {
    FORWARD,
    BACKWARD,
    LEFT,
    RIGHT,
    NONE
} check_direction = NONE;

int counter_ir = 0;

enum Step {
    BOOT,
    MATCH
} step = BOOT;


// Functions
void match_loop();

void process_match_commands();
// End functions

void process_ir_event();

void setup() {
    Serial.begin(9600);  // démarre le port série

    pinMode(PIN_TIRETTE, INPUT);

    pwm.begin();
    pwm.setOscillatorFrequency(27000000);
    pwm.setPWMFreq(50);

    pixels.begin();
    pixels.setBrightness(255);

    for (uint16_t i = 0; i < pixels.numPixels(); i++) {
        pixels.setPixelColor(i, red);
    }

    pixels.show();

    delay(1000);

}

void match_loop() {
    // Update obstacles sensors
    for (Sharp &sharp: sharps) {
        sharp.tick();
    }

    for (Servo &servo: servos) {
        servo.tick();
    }

    // Process serial commands
    process_match_commands();

    if (counter_ir++ % 50 == 0) {
        process_ir_event();
    }
}

void process_ir_event() {
    switch (check_direction) {
        case FORWARD:
            if (sharps[0].isBellow() || sharps[7].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+forward");
            }
            break;
        case LEFT:
            if (sharps[1].isBellow() || sharps[2].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+left");
            }
            break;
        case BACKWARD:
            if (sharps[3].isBellow() || sharps[4].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+backward");
            }
            break;
        case RIGHT:
            if (sharps[5].isBellow() || sharps[6].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+right");
            }
            break;
        case NONE:
            break;
    }
}

void process_match_commands() {
    if (Serial.available() <= 0) return; // No data available

    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith(COMMAND_PREFIX)) {
        command = command.substring(strlen(COMMAND_PREFIX));

        String command_name;
        String command_args;

        if (command.indexOf('=') == -1) {
            command_name = command;
            command_args = "";
        } else {
            command_name = command.substring(0, command.indexOf('='));
            command_args = command.substring(command.indexOf('=') + 1);
        }

        if (command_name == "ping") {
            Serial.println("R2+pong");
        } else if (command_name == "set_ir_direction") {
            if (command_args == "forward") {
                check_direction = FORWARD;
            } else if (command_args == "backward") {
                check_direction = BACKWARD;
            } else if (command_args == "left") {
                check_direction = LEFT;
            } else if (command_args == "right") {
                check_direction = RIGHT;
            } else if (command_args == "none") {
                check_direction = NONE;
            }
        } else if (command_name == "set_servo_angle") {
            long servo = command_args.substring(0, command_args.indexOf(',')).toInt();
            long angle = command_args.substring(command_args.indexOf(',') + 1).toInt();
            servos[servo].set_angle(angle);
        }
    }
}


void loop() {
    switch (step) {
        case BOOT:
            if (digitalRead(PIN_TIRETTE) == LOW) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("START");
                step = MATCH;
            }
        case MATCH:
            match_loop();
            break;
    }
    delay(10);
}