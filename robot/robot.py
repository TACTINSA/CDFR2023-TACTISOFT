import logging

from tactisoft.cli import NonBlockingCLI
from tactisoft.motors import Motors4
from tactisoft.movements import MecanumMovement
from tactisoft.sharedrobot import SharedRobot
from tactisoft.threadedserial import ThreadedSerial
from tactisoft import motors


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

    def register_commands(self, cli: NonBlockingCLI):
        super().register_commands(cli)
        cli.register_command("move", lambda x, y, z: self.movement.move(None if x == "null" else float(x), int(y), float(z)),
                             "Move in the given direction (in radians) at the given speed and turn [-1; 1]", "move <direction> <speed> <turn>")
        cli.register_command("forward", lambda x, y: self.movement.forward(int(x), int(y)), "Move forward at the given speed", "forward <speed>")
        cli.register_command("backward", lambda x: self.movement.backward(int(x)), "Move backward at the given speed", "backward <speed>")
        cli.register_command("right", lambda x: self.movement.right(int(x)), "Move right at the given speed", "right <speed>")
        cli.register_command("left", lambda x: self.movement.left(int(x)), "Move left at the given speed", "left <speed>")
        cli.register_command("stop", lambda: self.movement.stop(), "Stop the robot", "stop")
        cli.register_command("motor_raw", lambda *x: self.movement.send_command(motors.generate_command_with_validation(list(x))), "Send a raw command to the motor", "motor_raw <id> <command>")
