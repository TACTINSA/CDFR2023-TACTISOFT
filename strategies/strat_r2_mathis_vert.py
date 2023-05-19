import math
import time

from robot.robot_r2 import Robot

#Fermé/ouvert
# pince 1 : 10, 120 pince gauche id=0
# pince 2 : 175, 60 pince droite id=1 il vz dans le mauvais sens
# pont levis : 70, 25 id = 2 (PWM13)
def dist_to_time( distance:float):#la distance est exprimé en mm et le temps en secondes
    return distance/131
async def run(robot: Robot):
    time.sleep(1)
    robot.servos.set_servo_angle(0, 10)
    robot.servos.set_servo_angle(1, 175)
    robot.servos.set_servo_angle(2, 70)
    # robot.servos.set_servo_angle(0, 10)
    # print("1")
    # time.sleep(3)
    # robot.servos.set_servo_angle(0, 120)
    # print("2")
    # time.sleep(3)
    # robot.servos.set_servo_angle(1, 175)
    # print("3")
    # time.sleep(3)
    # robot.servos.set_servo_angle(1, 60)
    # print("4")
    # time.sleep(3)
    # robot.servos.set_servo_angle(2, 70)
    # print("5")
    # time.sleep(3)
    # robot.servos.set_servo_angle(2, 25)
    # print("6")
    # time.sleep(3)

    #Mouvement match 1

    await robot.movement.async_forward(speed=100, duration=dist_to_time(570))#étape 1
    await robot.movement.async_turn_right(speed=100, duration=1.45)#étape 2
    #ouverture pince
    robot.servos.set_servo_angle(0, 120)
    robot.servos.set_servo_angle(1, 60)
    await robot.movement.async_forward(speed=100, duration=dist_to_time(870))#etape3
    # robot.servos.set_servo_angle(0, 120)
    # robot.servos.set_servo_angle(1, 60)
    await robot.movement.async_move(direction=math.pi / 2, turn=1, speed=100, duration=2.3)#Etape4
    #await robot.movement.async_turn_right(speed=100, duration=1.40)
    await robot.movement.async_forward(speed=100, duration=dist_to_time(350))#Etape 5
    await robot.movement.async_turn_left(speed=100, duration=1.4)#Etape 6
    await robot.movement.async_forward(speed=100, duration=dist_to_time(170))#Etape 7
    await robot.movement.async_backward(speed=100, duration=dist_to_time(150))#Etape 8
    #fermeture pince
    robot.servos.set_servo_angle(0, 10)
    robot.servos.set_servo_angle(1, 175)
    await robot.movement.async_turn_left(speed=100, duration=1.4)#Etape 9
    await robot.movement.async_forward(speed=100, duration=dist_to_time(270))#Etape 10
    await robot.movement.async_right(speed=100, duration=dist_to_time(670),stop_ir_after=0)#Etape 11
    await robot.movement.async_backward(speed=100, duration=dist_to_time(300))#Etape 12
    await robot.movement.async_right(speed=100, duration=dist_to_time(50), stop_ir_after=0)#tape contre la paroie #Etape 13
    #Cesrise
    robot.servos.set_servo_angle(2, 70)
    time.sleep(0.5)
    robot.servos.set_servo_angle(2, 25)
    time.sleep(2)
    robot.servos.set_servo_angle(2, 70)
    time.sleep(0.5)

    await robot.movement.async_forward(speed=100, duration=dist_to_time(300))#Etape 14
    await robot.movement.async_left(speed=100, duration=dist_to_time(1650))#Etape 15#156cm de déplacement
    await robot.movement.async_backward(speed=100, duration=dist_to_time(350))#Etape 16

    return
    time.sleep(19000)


    #movement test
    while(1):
        await robot.movement.async_forward(speed=100, duration=1.5)
        await robot.movement.async_turn_right(speed=100, duration=1.5)
        await robot.movement.async_forward(speed=100, duration=1)
        await robot.movement.async_turn_right(speed=100, duration=3)
        await robot.movement.async_forward(speed=100, duration=1)
        await robot.movement.async_left(speed=100, duration=1.5)
    time.sleep(10000)
    await robot.movement.async_left(speed=100, duration=1)
    await robot.movement.async_turn_right(speed=100, duration=1.5)
    await robot.movement.async_stop()
    #movement + rotation en meme temps
    await robot.movement.async_move(direction=math.pi / 2, turn=1, speed=100, duration=2.3)
    #pince
    robot.servos.set_servo_angle(0, 120)
    robot.servos.set_servo_angle(1, 60)
    #pont levis
    robot.servos.set_servo_angle(2, 25)
    #sleep 1
    time.sleep(3)
    # Affichage dynamique
    robot.score = 50