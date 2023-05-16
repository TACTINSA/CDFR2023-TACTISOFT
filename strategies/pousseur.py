from robot.robot_r2 import Robot


async def run(robot: Robot):
    await robot.movement.async_left(speed=100, duration=5)
    await robot.movement.async_right(speed=100, duration=10)
    await robot.movement.async_left(speed=100, duration=5)

    await robot.movement.async_forward(speed=100, duration=5)
    await robot.movement.async_backward(speed=100, duration=10)
    await robot.movement.async_forward(speed=100, duration=5)
