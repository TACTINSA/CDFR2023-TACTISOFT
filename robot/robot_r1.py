import logging
import time

from tactisoft.cli import NonBlockingCLI
from tactisoft.motors import Motors3
from tactisoft.movements import OmniMovement
from tactisoft.sharedrobot import SharedRobot
from tactisoft.threadedserial import ThreadedSerial


class Robot(SharedRobot):
    def __init__(self):
        super().__init__("Robot Omni", "R1+")
        self.motors_serial = ThreadedSerial("/dev/motors", 38400, on_message=self.on_motor_message, raw=True)
        self.motors_ids = Motors3(mot1="e1", mot2="e2", mot3="e3")
        self.movement = OmniMovement(self.motors_serial, self.motors_ids, self.arduino)
        self.team = "unknown"

    def on_arduino_message(self, message):
        message: str = message
        if super().on_arduino_message(message):  # If handled by super don't handle the message
            return
        elif message.startswith("team"):
            self.team = message[5:]
        elif message.startswith("obstacle+%s" % self.movement.direction):
            # self.movement.obstacle_is_detected_flag = True
            while True:
                self.movement.stop()
                time.sleep(0.1)

    def on_motor_message(self, message):
        logging.debug("Motors -> Robot: " + " ".join(["{:02x}".format(x) for x in message]))

    def register_commands(self, cli: NonBlockingCLI):
        super().register_commands(cli)
        cli.register_command("move",
                             lambda x, y, z: self.movement.move(None if x == "null" else float(x), int(y), float(z)),
                             "Move in the given direction (in radians) at the given speed and turn [-1; 1]",
                             "move <direction> <speed> <turn>")
        cli.register_command("forward", lambda x: self.movement.forward(int(x)), "Move forward at the given speed",
                             "forward <speed>")
        cli.register_command("backward", lambda x: self.movement.backward(int(x)), "Move backward at the given speed",
                             "backward <speed>")
        cli.register_command("right", lambda x: self.movement.right(int(x)), "Move right at the given speed",
                             "right <speed>")
        cli.register_command("left", lambda x: self.movement.left(int(x)), "Move left at the given speed",
                             "left <speed>")
        cli.register_command("stop", lambda: self.movement.stop(), "Stop the robot", "stop")
