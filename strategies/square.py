from robot.robot import Robot


async def run(robot: Robot):
    await robot.movement.async_forward(speed=100, duration=4)
    await robot.movement.async_left(speed=100, duration=4)
    await robot.movement.async_backward(speed=100, duration=4)
    await robot.movement.async_right(speed=100, duration=4)
