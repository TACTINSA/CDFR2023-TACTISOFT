from robot.robot import Robot


# 10, 120
# 175, 60

async def run(robot: Robot):
    robot.servos.set_servo_angle(0, 120)
    robot.servos.set_servo_angle(1, 60)
    await robot.movement.async_forward(speed=100, duration=4)
    robot.servos.set_servo_angle(0, 10)
    robot.servos.set_servo_angle(1, 175)
    await robot.movement.async_left(speed=100, duration=4)
    await robot.movement.async_backward(speed=100, duration=4)
    await robot.movement.async_right(speed=100, duration=4)
