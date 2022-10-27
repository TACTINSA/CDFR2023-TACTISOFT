import math

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

    def move(self, angle: float, speed: int, rotation: float = 0, distance: int = None):
        """Move the robot in the given angle (in radians) for the specified distance or indefinitely if none given"""
        front_right_and_back_left = math.sin(angle - math.pi / 4) * speed
        front_left_and_back_right = math.sin(angle + math.pi / 4) * speed

        if front_right_and_back_left != 0:
            self.send_command(motors.move(motor_id=self.motor_ids.front_right,
                                          direction=get_direction(front_right_and_back_left, True),
                                          speed=abs(int(front_right_and_back_left)),
                                          distance=distance))
            self.send_command(motors.move(motor_id=self.motor_ids.back_left,
                                          direction=get_direction(front_right_and_back_left, False),
                                          speed=abs(int(front_right_and_back_left)),
                                          distance=distance))
        else:
            self.send_command(motors.stop(self.motor_ids.front_right))
            self.send_command(motors.stop(self.motor_ids.back_left))

        if front_left_and_back_right != 0:
            self.send_command(motors.move(motor_id=self.motor_ids.front_left,
                                          direction=get_direction(front_left_and_back_right, False),
                                          speed=abs(int(front_left_and_back_right)),
                                          distance=distance))
            self.send_command(motors.move(motor_id=self.motor_ids.back_right,
                                          direction=get_direction(front_left_and_back_right, True),
                                          speed=abs(int(front_left_and_back_right)),
                                          distance=distance))
        else:
            self.send_command(motors.stop(self.motor_ids.front_left))
            self.send_command(motors.stop(self.motor_ids.back_right))

    def forward(self, speed: int, distance: int = None):
        self.move(angle=math.pi / 2, speed=speed, distance=distance)

    def backward(self, speed: int, distance: int = None):
        self.move(angle=3 * math.pi / 2, speed=speed, distance=distance)

    def right(self, speed: int, distance: int = None):
        self.move(angle=0, speed=speed, distance=distance)

    def left(self, speed: int, distance: int = None):
        self.move(angle=math.pi, speed=speed, distance=distance)
