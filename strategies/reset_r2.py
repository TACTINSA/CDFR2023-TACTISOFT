from robot.robot_r2 import Robot


async def run(robot: Robot):
    robot.servos.set_servo_angle(0, 10)
    robot.servos.set_servo_angle(1, 175)
    robot.servos.set_servo_angle(2, 70)

    robot.arduino.send("R2+set_led_color=purple")

    while True:
        pass
