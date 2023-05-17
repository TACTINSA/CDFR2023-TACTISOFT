import logging

from robot.robot_r2 import Robot


# pince 1 : 10, 120
# pince 2 : 175, 60
# pont levis : 70, 25

async def run(robot: Robot):
    await robot.movement.async_forward(speed=100, duration=5)
    robot.score = 11
