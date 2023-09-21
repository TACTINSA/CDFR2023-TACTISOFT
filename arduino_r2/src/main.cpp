#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <tacticom.h>

#include <servos/Software_I2C_Adafruit_PWMServoDriver.h>
#include "sharps/sharp.h"
#include "servos/servo.h"

#define COMMAND_PREFIX "R2"
#define DISTANCE_DETECTION 20

#define PIN_TIRETTE 2
#define PIN_LED 6
#define PIN_LED_DEGUISEMENT 10

#define NB_LEDS (9 * 4)
#define NB_LEDS_DEGUISEMENT 27

uint32_t red = Adafruit_NeoPixel::Color(255, 0, 0);
uint32_t purple = Adafruit_NeoPixel::Color(165, 50, 150);
uint32_t blue = Adafruit_NeoPixel::Color(0, 92, 230);
uint32_t green = Adafruit_NeoPixel::Color(0, 170, 18);
Adafruit_NeoPixel pixels(NB_LEDS, PIN_LED, NEO_GRB);
Adafruit_NeoPixel pixels_deguisement(NB_LEDS_DEGUISEMENT, PIN_LED_DEGUISEMENT, NEO_GRB);

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
        Servo(pwm, 14, 0, 270),
        Servo(pwm, 15, 0, 270),
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
    MATCH,
    END
} step = BOOT;


// Functions
void match_loop();

void process_match_commands();
// End functions

void process_ir_event();

void set_led_colors(uint32_t color);

void deguisement();

void whiteOverRainbow(int whiteSpeed, int whiteLength);

void router(const String &name, const String args[], uint8_t args_count);

Tacticom tacticom(router, COMMAND_PREFIX);

void setup() {
    Serial.begin(9600);  // démarre le port série

    pinMode(PIN_TIRETTE, INPUT);

    pwm.begin();
    pwm.setOscillatorFrequency(27000000);
    pwm.setPWMFreq(50);

    pixels.begin();
    pixels.setBrightness(255);

    pixels_deguisement.begin();
    pixels_deguisement.show();

    set_led_colors(purple);

    delay(1000);
}

void set_led_colors(uint32_t color) {
    for (uint16_t i = 0; i < pixels.numPixels(); i++) {
        pixels.setPixelColor(i, color);
    }

    pixels.show();
}

void match_loop() {
    // Process serial commands
    tacticom.tick();

    // Update obstacles sensors
    for (Sharp &sharp: sharps) {
        sharp.tick();
    }

    for (Servo &servo: servos) {
        servo.tick();
    }

    if (counter_ir++ % 50 == 0) {
        process_ir_event();
    }
}

void process_ir_event() {
    switch (check_direction) {
        case FORWARD:
            if (sharps[0].isBellow() || sharps[7].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.print("obstacle+forward+");
                Serial.print(sharps[0].getDistance());
                Serial.print(",");
                Serial.println(sharps[7].getDistance());
            }
            break;
        case LEFT:
            if (sharps[1].isBellow() || sharps[2].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.print("obstacle+left+");
                Serial.print(sharps[1].getDistance());
                Serial.print(",");
                Serial.println(sharps[2].getDistance());
            }
            break;
        case BACKWARD:
            if (sharps[3].isBellow() || sharps[4].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.print("obstacle+backward+");
                Serial.print(sharps[3].getDistance());
                Serial.print(",");
                Serial.println(sharps[4].getDistance());
            }
            break;
        case RIGHT:
            if (sharps[5].isBellow() || sharps[6].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.print("obstacle+right+");
                Serial.print(sharps[5].getDistance());
                Serial.print(",");
                Serial.println(sharps[6].getDistance());
            }
            break;
        case NONE:
            break;
    }
}

void router(const String &name, const String args[], uint8_t args_count) {
    if (name == "ping") {
        tacticom.send("pong");
    } else if (name == "set_ir_direction") {
        if (args_count != 1)
            return;

        if (args[0] == "forward") {
            check_direction = FORWARD;
        } else if (args[0] == "backward") {
            check_direction = BACKWARD;
        } else if (args[0] == "left") {
            check_direction = LEFT;
        } else if (args[0] == "right") {
            check_direction = RIGHT;
        } else if (args[0] == "none") {
            check_direction = NONE;
        }
    } else if (name == "set_servo_angle") {
        if (args_count != 2)
            return;

        long servo = args[0].toInt();
        long angle = args[1].toInt();
        servos[servo].set_angle(angle);
    } else if (name == "set_led_color") {
        if (args_count != 1)
            return;

        if (args[0] == "green") {
            set_led_colors(green);
        } else if (args[0] == "blue") {
            set_led_colors(blue);
        } else if (args[0] == "red") {
            set_led_colors(red);
        } else if (args[0] == "purple") {
            set_led_colors(purple);
        }
    } else if (name == "finish_match") {
        step = END;
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
        case END:
            set_led_colors(red);
            deguisement();
            break;
    }
    delay(10);
}

void deguisement() {
    whiteOverRainbow(75, 5);
}

void whiteOverRainbow(int whiteSpeed, int whiteLength) {

    if (whiteLength >= pixels_deguisement.numPixels()) whiteLength = pixels_deguisement.numPixels() - 1;

    int head = whiteLength - 1;
    int tail = 0;
    int loops = 3;
    int loopNum = 0;
    uint32_t lastTime = millis();
    uint32_t firstPixelHue = 0;

    for (;;) { // Repeat forever (or until a 'break' or 'return')
        for (int i = 0; i < pixels_deguisement.numPixels(); i++) {  // For each pixel in strip...
            if (((i >= tail) && (i <= head)) ||      //  If between head & tail...
                ((tail > head) && ((i >= tail) || (i <= head)))) {
                pixels_deguisement.setPixelColor(i, pixels_deguisement.Color(0, 0, 0, 255)); // Set white
            } else {                                             // else set rainbow
                int pixelHue = firstPixelHue + (i * 65536L / pixels_deguisement.numPixels());
                pixels_deguisement.setPixelColor(i, pixels_deguisement.gamma32(pixels_deguisement.ColorHSV(pixelHue)));
            }
        }

        pixels_deguisement.show(); // Update strip with new contents
        // There's no delay here, it just runs full-tilt until the timer and
        // counter combination below runs out.

        firstPixelHue += 40; // Advance just a little along the color wheel

        if ((millis() - lastTime) > whiteSpeed) { // Time to update head/tail?
            if (++head >= pixels_deguisement.numPixels()) {      // Advance head, wrap around
                head = 0;
                if (++loopNum >= loops) return;
            }
            if (++tail >= pixels_deguisement.numPixels()) {      // Advance tail, wrap around
                tail = 0;
            }
            lastTime = millis();                   // Save time of last movement
        }
    }
}

