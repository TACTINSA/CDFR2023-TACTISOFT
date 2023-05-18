import asyncio
import logging
import math
import time
from typing import Optional

from tactisoft import motors
from tactisoft.motors import Motors4, Direction, Motors3
from tactisoft.threadedserial import ThreadedSerial


def get_direction(speed: float, inverted: bool) -> Direction:
    return Direction.FORWARD if (
                                        speed > 0) ^ inverted else Direction.BACKWARD  # ^ is xor (exclusive or) to return the opposite of the direction if the motor is inverted


class MecanumMovement:
    def __init__(self, serial: ThreadedSerial, motor_ids: Motors4, arduino: ThreadedSerial):
        self.obstacle_is_detected_flag = False
        self.motor_ids = motor_ids
        self.serial = serial
        self.arduino = arduino
        self.direction = "none"

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

    async def async_move(self, duration: float, direction: Optional[float], speed: int, turn: float = 0, stop_ir_after: int = None):
        """Move the robot in the given direction (in radians) for the specified distance or indefinitely if none given and turn [-1; 1]"""
        assert speed > 0, "Speed must be positive"

        start_time = time.time()
        self.move(direction=direction, speed=speed, turn=turn)

        while time.time() - start_time < duration:
            if self.obstacle_is_detected_flag:
                if stop_ir_after is not None and time.time() - start_time > stop_ir_after:
                    continue
                else:
                    duration = duration - (time.time() - start_time)
                    if stop_ir_after is not None:
                        stop_ir_after = stop_ir_after - (time.time() - start_time)

                    self.stop()
                    while self.obstacle_is_detected_flag:
                        self.obstacle_is_detected_flag = False
                        await asyncio.sleep(1)
                    start_time = time.time()
                    self.move(direction=direction, speed=speed, turn=turn)

            await asyncio.sleep(0.1)

        self.stop()
        self.arduino.send("R2+set_ir_direction=none")

    def forward(self, speed: int, distance: int = None):
        self.move(direction=math.pi / 2, speed=speed, distance=distance)

    async def async_forward(self, speed: int, duration: float, stop_ir_after: int = None):
        self.set_direction("forward")
        await self.async_move(duration=duration, direction=math.pi / 2, speed=speed, stop_ir_after=stop_ir_after)

    def backward(self, speed: int, distance: int = None):
        self.move(direction=3 * math.pi / 2, speed=speed, distance=distance)

    async def async_backward(self, speed: int, duration: float, stop_ir_after: int = None):
        self.set_direction("backward")
        await self.async_move(duration=duration, direction=3 * math.pi / 2, speed=speed, stop_ir_after=stop_ir_after)

    def right(self, speed: int, distance: int = None):
        self.move(direction=0, speed=speed, distance=distance)

    async def async_right(self, speed: int, duration: float, stop_ir_after: int = None):
        self.set_direction("right")
        await self.async_move(duration=duration, direction=0, speed=speed, stop_ir_after=stop_ir_after)

    def left(self, speed: int, distance: int = None):
        self.move(direction=math.pi, speed=speed, distance=distance)

    async def async_left(self, speed: int, duration: float, stop_ir_after: int = None):
        self.set_direction("left")
        await self.async_move(duration=duration, direction=math.pi, speed=speed, stop_ir_after=stop_ir_after)

    def turn_right(self, speed: int, distance: int = None):
        self.move(direction=None, speed=speed, turn=1, distance=distance)

    async def async_turn_right(self, speed: int, duration: float, stop_ir_after: int = None):
        await self.async_move(duration=duration, direction=None, speed=speed, turn=1, stop_ir_after=stop_ir_after)

    def turn_left(self, speed: int, distance: int = None):
        self.move(direction=None, speed=speed, turn=-1, distance=distance)

    async def async_turn_left(self, speed: int, duration: float, stop_ir_after: int = None):
        await self.async_move(duration=duration, direction=None, speed=speed, turn=-1, stop_ir_after=stop_ir_after)

    def stop(self):
        self.send_command(motors.stop(self.motor_ids.front_right))
        self.send_command(motors.stop(self.motor_ids.front_left))
        self.send_command(motors.stop(self.motor_ids.back_right))
        self.send_command(motors.stop(self.motor_ids.back_left))

    async def async_stop(self):
        self.stop()
        self.arduino.send("R2+set_ir_direction=none")

    def set_direction(self, direction: str):
        self.arduino.send("R2+set_ir_direction=%s" % direction)
        self.direction = direction


class OmniMovement:
    def __init__(self, serial: ThreadedSerial, motor_ids: Motors3, arduino: ThreadedSerial):
        self.motor_ids = motor_ids
        self.serial = serial
        self.direction = "none"
        self.arduino = arduino

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

    def angle_0(self, speed: int, duration: int = None): # direction mouton minecraft, IR_1 A8
        self.set_direction("angle_0")
        self.move_wheel(self.motor_ids.mot1, speed, direction = False)
        self.move_wheel(self.motor_ids.mot2, speed, direction = True)
        self.send_command(motors.stop(self.motor_ids.mot3))

    def angle_60(self, speed: int, duration: int = None):  # direction bouton choix équipe, IR_2 A11
        self.set_direction("angle_60")
        self.send_command(motors.stop(self.motor_ids.mot1))
        self.move_wheel(self.motor_ids.mot2, speed, direction=True)
        self.move_wheel(self.motor_ids.mot3, speed, direction=False)

    def angle_120(self, speed: int, duration: int = None):  # direction batterie logique, IR_5 A10
        self.set_direction("angle_120")
        self.move_wheel(self.motor_ids.mot1, speed, direction=True)
        self.send_command(motors.stop(self.motor_ids.mot2))
        self.move_wheel(self.motor_ids.mot3, speed, direction=False)

    def angle_180(self, speed: int, duration: int = None): # direction bouton arrêt d'urgence, IR_6 A13
        self.set_direction("angle_180")
        self.move_wheel(self.motor_ids.mot1, speed, direction = True)
        self.move_wheel(self.motor_ids.mot2, speed, direction = False)
        self.send_command(motors.stop(self.motor_ids.mot3))

    def angle_240(self, speed: int, duration: int = None):  # direction batterie actionneurs, IR_3 A9
        self.set_direction("angle_240")
        self.send_command(motors.stop(self.motor_ids.mot1))
        self.move_wheel(self.motor_ids.mot2, speed, direction=False)
        self.move_wheel(self.motor_ids.mot3, speed, direction=True)

    def angle_300(self, speed: int, duration: int = None):  # direction tirette, IR_4 A12
        self.set_direction("angle_300")
        self.move_wheel(self.motor_ids.mot1, speed, direction=False)
        self.send_command(motors.stop(self.motor_ids.mot2))
        self.move_wheel(self.motor_ids.mot3, speed, direction=True)

    def rotation_gauche(self, speed: int, duration: int = None):
        self.set_direction("rotation_gauche")
        self.move_wheel(self.motor_ids.mot1, speed, direction=False)
        self.move_wheel(self.motor_ids.mot2, speed, direction=False)
        self.move_wheel(self.motor_ids.mot3, speed, direction=False)

    def rotation_droite(self, speed: int, duration: int = None):
        self.set_direction("rotation_gauche")
        self.move_wheel(self.motor_ids.mot1, speed, direction=True)
        self.move_wheel(self.motor_ids.mot2, speed, direction=True)
        self.move_wheel(self.motor_ids.mot3, speed, direction=True)





    def turn_right(self, speed: int, distance: int = None):
        self.move(direction=None, speed=speed, turn=1, distance=distance)

    def turn_left(self, speed: int, distance: int = None):
        self.move(direction=None, speed=speed, turn=-1, distance=distance)

    def stop(self):
        self.send_command(motors.stop(self.motor_ids.mot1))
        self.send_command(motors.stop(self.motor_ids.mot2))
        self.send_command(motors.stop(self.motor_ids.mot3))

    def set_direction(self, direction: str):
        self.arduino.send("R1+set_ir_direction=%s" % direction)
        self.direction = direction
