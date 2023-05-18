import math
import time

from robot.robot_r2 import Robot


# pince 1 : 10, 120
# pince 2 : 175, 60
# pont levis : 70, 25

async def run(robot: Robot):
    await robot.movement.async_forward(speed=100, duration=4.5)
    await robot.movement.async_turn_left(speed=100, duration=1.5)
    robot.servos.set_servo_angle(0, 120)
    robot.servos.set_servo_angle(1, 60)
    await robot.movement.async_forward(speed=100, duration=6)
    await robot.movement.async_move(direction=math.pi / 2, turn=-1, speed=100, duration=2.3)
    await robot.movement.async_forward(speed=100, duration=2.5)
    await robot.movement.async_turn_right(speed=100, duration=1.3)
    await robot.movement.async_forward(speed=100, duration=2)
    await robot.movement.async_backward(speed=100, duration=1)
    robot.servos.set_servo_angle(0, 10)
    robot.servos.set_servo_angle(1, 175)
    await robot.movement.async_turn_left(speed=100, duration=1.4)
    await robot.movement.async_backward(speed=100, duration=2)
    await robot.movement.async_right(speed=100, duration=4.4, stop_ir_after=0)
    await robot.movement.async_forward(speed=100, duration=2)
    await robot.movement.async_right(speed=100, duration=1, stop_ir_after=0)
    await robot.movement.async_stop()
    robot.servos.set_servo_angle(2, 25)
    time.sleep(3)
    await robot.movement.async_left(speed=100, duration=0.5)
    await robot.movement.async_backward(speed=100, duration=3)
    await robot.movement.async_left(speed=100, duration=4.4)
    await robot.movement.async_forward(speed=100, duration=2)
    await robot.movement.async_left(speed=100, duration=10)
    await robot.movement.async_stop()
    robot.servos.set_servo_angle(0, 10)
    robot.servos.set_servo_angle(1, 175)
    robot.servos.set_servo_angle(2, 70)

