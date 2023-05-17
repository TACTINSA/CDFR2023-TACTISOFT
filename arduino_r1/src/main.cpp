#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#include "sharps/sharp.h"
#include "Adafruit_PWMServoDriver.h"


#define COMMAND_PREFIX "R1+"
#define DISTANCE_DETECTION 30

#define PIN_TIRETTE 53
#define PIN_LED 6

#define BTN_BLEUE 24
#define BTN_VERT 22


// Servos
#define SERVOMIN  80 // Position minimale
#define SERVOMAX  530 // Position maximale

#define MOYENNE ((SERVOMIN + SERVOMAX) / 2)

#define STANDBY_0 (MOYENNE - 115) // Servo 0
#define STANDBY_1 (MOYENNE + 102) // Servo 1
#define STANDBY_2 (MOYENNE - 120) // Servo 2
#define STANDBY_3 (MOYENNE + 105) // Servo 3
#define STANDBY_4 (MOYENNE - 120) // Servo 4
#define STANDBY_5 (MOYENNE + 120) // Servo 5

#define FERMETURE 150
#define OUVERTURE 250
#define STANDBY 0

#define GARDE_CERISE 0 // servos cerises : 6 7 8
#define DEPOSE_CERISE 0

Adafruit_PWMServoDriver servo = Adafruit_PWMServoDriver();

// LEDS
#define PIN_LEDS 6
#define NUMPIXELS 15
uint32_t equipe_verte = Adafruit_NeoPixel::Color(0, 170, 18);
uint32_t equipe_bleue = Adafruit_NeoPixel::Color(0, 92, 230);
uint32_t pas_dequipe = Adafruit_NeoPixel::Color(165, 50, 150);
Adafruit_NeoPixel led = Adafruit_NeoPixel(NUMPIXELS, PIN_LEDS, NEO_GRB + NEO_KHZ800);


// Sharps
Sharp sharps[] = {
        Sharp(A8, DISTANCE_DETECTION),
        Sharp(A11, DISTANCE_DETECTION),
        Sharp(A10, DISTANCE_DETECTION),
        Sharp(A13, DISTANCE_DETECTION),
        Sharp(A9, DISTANCE_DETECTION),
        Sharp(A12, DISTANCE_DETECTION),
};


/*--------CAPTEURS COULEUR----------*/

#include "Adafruit_TCS34725softi2c.h"

//CAPTEUR COULEUR 1 : face batterie logique
//SCL sur digital, SDA sur digital, GND et 5V

#define SDA1 50
#define SCL1 52
Adafruit_TCS34725softi2c tcs1 = Adafruit_TCS34725softi2c(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X, SDA1, SCL1);

//CAPTEUR COULEUR 2 : face batterie actionneur
//SCL sur digital, SDA sur digital, GND et 5V

#define SDA2 46
#define SCL2 48
Adafruit_TCS34725softi2c tcs2 = Adafruit_TCS34725softi2c(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X, SDA2, SCL2);

//CAPTEUR COULEUR 3 : face vide / mouton
//SCL sur digital, SDA sur digital, GND et 5V

#define SDA3 42
#define SCL3 44
Adafruit_TCS34725softi2c tcs3 = Adafruit_TCS34725softi2c(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X, SDA3, SCL3);


enum check_direction {
    ANGLE_0,
    ANGLE_60,
    ANGLE_120,
    ANGLE_180,
    ANGLE_240,
    ANGLE_300,
    NONE
} check_direction = NONE;

enum team {
    VERT,
    BLEU,
    NO_TEAM
} team = NO_TEAM;

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

void pince_management(byte num_pince, int commande);

void couleur_LEDS(uint32_t couleur);


void setup() {
    led.begin();
    led.setBrightness(255);
    led.show(); // Initialize all pixels to 'off'

    servo.begin();
    Serial.begin(9600);
    servo.setOscillatorFrequency(27000000);
    servo.setPWMFreq(50);

    tcs1.begin();
    tcs2.begin();
    tcs3.begin();

    pinMode(PIN_TIRETTE, INPUT_PULLUP);
    pinMode(BTN_BLEUE, INPUT_PULLUP);
    pinMode(BTN_VERT, INPUT_PULLUP);

    couleur_LEDS(pas_dequipe);

    pince_management(1, STANDBY);
    pince_management(2, STANDBY);
    pince_management(3, STANDBY);

    delay(1000);
}

void match_loop() {
    // Update obstacles sensors
    for (Sharp &sharp: sharps) {
        sharp.tick();
    }

    // Process serial commands
    process_match_commands();

    if (counter_ir++ % 50 == 0) {
        process_ir_event();
    }
}

void process_ir_event() {
    switch (check_direction) {
        case ANGLE_0:
            if (sharps[0].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+angle_0");
            }
            break;
        case ANGLE_60:
            if (sharps[1].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+angle_60");
            }
            break;
        case ANGLE_120:
            if (sharps[2].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+angle_120");
            }
            break;
        case ANGLE_180:
            if (sharps[3].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+angle_180");
            }
            break;
        case ANGLE_240:
            if (sharps[4].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+angle_240");
            }
            break;
        case ANGLE_300:
            if (sharps[5].isBellow()) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("obstacle+angle_300");
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
            Serial.println("R1+pong");
        } else if (command_name == "set_ir_direction") {
            if (command_args == "angle_0") {
                check_direction = ANGLE_0;
            } else if (command_args == "angle_60") {
                check_direction = ANGLE_60;
            } else if (command_args == "angle_120") {
                check_direction = ANGLE_120;
            } else if (command_args == "angle_180") {
                check_direction = ANGLE_180;
            } else if (command_args == "angle_240") {
                check_direction = ANGLE_240;
            } else if (command_args == "angle_300") {
                check_direction = ANGLE_300;
            } else if (command_args == "none") {
                check_direction = NONE;
            }
        } else if (command_name == "set_pince_commande") {
            byte pince = command_args.substring(0, command_args.indexOf(',')).toInt();
            int commande = (int) command_args.substring(command_args.indexOf(',') + 1).toInt();
            pince_management(pince, commande);
        } else if (command_name == "get_team") {
            Serial.print(COMMAND_PREFIX);
            Serial.print("team=");
            if (team == VERT) {
                Serial.println("vert");
            } else if (team == BLEU) {
                Serial.println("bleu");
            } else {
                Serial.println("none");
            }
        }
    }
}


void loop() {
    switch (step) {
        case BOOT:
            if (digitalRead(PIN_TIRETTE) == HIGH) {
                Serial.print(COMMAND_PREFIX);
                Serial.println("START");
                step = MATCH;
            }
            if (digitalRead(BTN_BLEUE) == LOW) {
                team = BLEU;
                couleur_LEDS(equipe_bleue);
            } else if (digitalRead(BTN_VERT) == LOW) {
                team = VERT;
                couleur_LEDS(equipe_verte);
            } else {
                team = NO_TEAM;
                couleur_LEDS(pas_dequipe);
            }
            break;
        case MATCH:
            match_loop();
            break;
    }
    delay(10);
}

void couleur_LEDS(uint32_t couleur) {
    led.clear();
    for (int i = 0; i < NUMPIXELS; i++)
        led.setPixelColor(i, couleur);
    led.show();
}

void pince_management(byte num_pince, int commande) {
    switch (num_pince) {
        case 1:
            servo.setPWM(0, 0, STANDBY_0 + commande);
            servo.setPWM(1, 0, STANDBY_1 - commande);
            break;

        case 2:
            servo.setPWM(2, 0, STANDBY_2 + commande);
            servo.setPWM(3, 0, STANDBY_3 - commande);
            break;

        case 3:
            servo.setPWM(4, 0, STANDBY_4 + commande);
            servo.setPWM(5, 0, STANDBY_5 - commande);
            break;
    }
}
