from robot.robot import Robot


# pince 1 : 10, 120
# pince 2 : 175, 60
# pont levis : 70, 25

async def run(robot: Robot):
    robot.servos.set_servo_angle(0, 120)
    robot.servos.set_servo_angle(1, 60)
    await robot.movement.async_forward(speed=100, duration=15, stop_ir_after=10)
    robot.servos.set_servo_angle(0, 10)
    robot.servos.set_servo_angle(1, 175)
    await robot.movement.async_left(speed=100, duration=4)
    await robot.movement.async_backward(speed=100, duration=4)
    await robot.movement.async_right(speed=100, duration=4)
