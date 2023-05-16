import time

from robot.robot_r2 import Robot
from tactisoft import motors
from tactisoft.motors import Direction

speed = 100


async def run(robot: Robot):
    robot.movement.send_command(motors.stop(motor_id="e1"))
    robot.movement.send_command(motors.stop(motor_id="e2"))
    robot.movement.send_command(motors.stop(motor_id="e3"))
    while (True):
        robot.movement.send_command(motors.move(motor_id="e1", direction=Direction.FORWARD, speed=speed))
        robot.movement.send_command(motors.move(motor_id="e2", direction=Direction.BACKWARD, speed=speed))
        robot.movement.send_command(motors.stop(motor_id="e3"))
        time.sleep(5)
        robot.movement.send_command(motors.move(motor_id="e1", direction=Direction.BACKWARD, speed=speed))
        robot.movement.send_command(motors.move(motor_id="e2", direction=Direction.FORWARD, speed=speed))
        robot.movement.send_command(motors.stop(motor_id="e3"))
        time.sleep(5)
        robot.movement.send_command(motors.move(motor_id="e1", direction=Direction.BACKWARD, speed=speed))
        robot.movement.send_command(motors.move(motor_id="e2", direction=Direction.BACKWARD, speed=speed))
        robot.movement.send_command(motors.move(motor_id="e3", direction=Direction.BACKWARD, speed=speed))
        time.sleep(10.7)

    # robot.movement.send_command(motors.move(motor_id="e3", direction=Direction.FORWARD, speed=50))
