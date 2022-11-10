import logging
import math
from typing import Optional

from tactisoft import motors
from tactisoft.motors import Motors4, Direction
from tactisoft.threadedserial import ThreadedSerial


def get_direction(speed: float, inverted: bool) -> Direction:
    return Direction.FORWARD if (speed > 0) ^ inverted else Direction.BACKWARD  # ^ is xor (exclusive or) to return the opposite of the direction if the motor is inverted


class MecanumMovement:
    def __init__(self, serial: ThreadedSerial, motor_ids: Motors4):
        self.motor_ids = motor_ids
        self.serial = serial

    def send_command(self, command):
        self.serial.send(bytes.fromhex(command))

    def move_wheel(self, motor_id: str, speed: float, direction: bool, distance: int = None):
        logging.debug("Moving motor %s in direction %f at speed %d" % (motor_id, direction, speed))
        if abs(int(speed)) != 0:
            self.send_command(motors.move(motor_id=motor_id,
                                          direction=get_direction(speed, direction),
                                          speed=abs(int(speed)),
                                          distance=distance))
        else:
            self.send_command(motors.stop(motor_id))

    def move(self, direction: Optional[float], speed: int, turn: float = 0, distance: int = None):
        """Move the robot in the given direction (in radians) for the specified distance or indefinitely if none given and turn [-1; 1]"""
        assert speed > 0, "Speed must be positive"

        if direction is not None:
            front_right_and_back_left = math.sin(direction - math.pi / 4)
            front_left_and_back_right = math.sin(direction + math.pi / 4)
        else:
            front_right_and_back_left = 0
            front_left_and_back_right = 0

        front_right = front_right_and_back_left - turn
        front_left = front_left_and_back_right + turn
        back_right = front_left_and_back_right - turn
        back_left = front_right_and_back_left + turn

        max_value = max(abs(front_right), abs(front_left), abs(back_right), abs(back_left))
        if max_value > 1:
            front_right /= max_value
            front_left /= max_value
            back_right /= max_value
            back_left /= max_value

        self.move_wheel(self.motor_ids.front_right, front_right * speed, True, distance)
        self.move_wheel(self.motor_ids.front_left, front_left * speed, False, distance)
        self.move_wheel(self.motor_ids.back_right, back_right * speed, True, distance)
        self.move_wheel(self.motor_ids.back_left, back_left * speed, False, distance)

    def forward(self, speed: int, distance: int = None):
        self.move(direction=math.pi / 2, speed=speed, distance=distance)

    def backward(self, speed: int, distance: int = None):
        self.move(direction=3 * math.pi / 2, speed=speed, distance=distance)

    def right(self, speed: int, distance: int = None):
        self.move(direction=0, speed=speed, distance=distance)

    def left(self, speed: int, distance: int = None):
        self.move(direction=math.pi, speed=speed, distance=distance)

    def turn_right(self, speed: int, distance: int = None):
        self.move(direction=None, speed=speed, turn=1, distance=distance)

    def turn_left(self, speed: int, distance: int = None):
        self.move(direction=None, speed=speed, turn=-1, distance=distance)

    def stop(self):
        self.send_command(motors.stop(self.motor_ids.front_right))
        self.send_command(motors.stop(self.motor_ids.front_left))
        self.send_command(motors.stop(self.motor_ids.back_right))
        self.send_command(motors.stop(self.motor_ids.back_left))
