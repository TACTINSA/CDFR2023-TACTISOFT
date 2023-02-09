import time

from robot.robot import Robot


def run(robot: Robot):
    # robot.movement.turn_left(speed=100)
    robot.movement.forward(speed=100)
    time.sleep(3)
    robot.movement.stop()
