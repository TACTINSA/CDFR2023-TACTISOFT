import logging

from tactisoft.motors import Motors4
from tactisoft.movements import MecanumMovement
from tactisoft.sharedrobot import SharedRobot
from tactisoft.threadedserial import ThreadedSerial


class Robot(SharedRobot):
    def __init__(self):
        super().__init__("Robot 1")
        self.motors_serial = ThreadedSerial("/dev/ttyUSB0", 38400, on_message=self.on_motor_message, raw=True, prefix="R2+")
        self.motors_ids = Motors4(front_right="e1", front_left="e2", back_right="e3", back_left="e4")
        self.movement = MecanumMovement(self.motors_serial, self.motors_ids)

    def on_arduino_message(self, message):
        if super().on_arduino_message(message):  # If handled by super don't handle the message
            return
        elif message.startswith():
            pass

    def on_motor_message(self, message):
        logging.debug("Motors -> Robot: " + " ".join(["{:02x}".format(x) for x in message]))
