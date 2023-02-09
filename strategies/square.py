import time

from robot.robot import Robot


def run(robot: Robot):
    while True:
        robot.movement.forward(speed=100)
        time.sleep(2)
        robot.movement.left(speed=100)
        time.sleep(2)
        robot.movement.backward(speed=100)
        time.sleep(2)
        robot.movement.right(speed=100)
        time.sleep(2)
        robot.movement.stop()
        time.sleep(2)
