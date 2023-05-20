import logging
import time

from robot.robot_r1 import Robot


def set_pince_commande(robot: Robot, pince: int, commande: str):
    if commande == "OUVERTURE":
        robot.arduino.send("R1+set_pince_commande=%s,%s" % (pince, 250))
    elif commande == "STANDBY":
        robot.arduino.send("R1+set_pince_commande=%s,%s" % (pince, 0))
    elif commande == "FERMETURE":
        robot.arduino.send("R1+set_pince_commande=%s,%s" % (pince, 150))


async def strat_bleu(robot: Robot):
    # commence sur la case bleue à côté des cerises perpendiculaires
    set_pince_commande(robot, 1, "STANDBY")
    set_pince_commande(robot, 2, "STANDBY")
    set_pince_commande(robot, 3, "STANDBY")
    set_pince_commande(robot, 4, "STANDBY")
    set_pince_commande(robot, 5, "STANDBY")
    set_pince_commande(robot, 6, "STANDBY")

    set_pince_commande(robot, 1, "OUVERTURE")
    await robot.movement.async_angle_0(110, 4.7)  # Etape 1
    set_pince_commande(robot, 1, "FERMETURE")
    time.sleep(0.5)
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 /3)  # Etape 2
    set_pince_commande(robot, 2, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_120(110, 2)  # Etape 1
    set_pince_commande(robot, 2, "FERMETURE")
    time.sleep(0.5)
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 /2)  # Etape 2
    set_pince_commande(robot, 3, "OUVERTURE")
    await robot.movement.async_angle_240(110, 6)  # Etape 1
    set_pince_commande(robot, 3, "FERMETURE")
    time.sleep(0.5)
    await robot.movement.async_angle_180(110, 5)  # Etape 1
    await robot.movement.async_angle_120(110, 4.5)  # Etape 1

    set_pince_commande(robot, 2, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_300(110, 1.5)  # étape 10
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 / 3)  # étape 11
    await robot.movement.async_angle_240(110, 1)  # étape 12
    set_pince_commande(robot, 3, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_60(110, 1)  # étape 13
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 / 3)  # étape 14
    await robot.movement.async_angle_0(110, 1)  # étape 15
    set_pince_commande(robot, 1, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_180(110, 1)  # étape 13
    # time.sleep(18) # TODO Add to make robot wait for the other one
    await robot.movement.async_angle_120(110, 4.2)  # étape 13


async def strat_vert(robot: Robot):
    set_pince_commande(robot, 1, "STANDBY")
    set_pince_commande(robot, 2, "STANDBY")
    set_pince_commande(robot, 3, "STANDBY")
    set_pince_commande(robot, 4, "STANDBY")
    set_pince_commande(robot, 5, "STANDBY")
    set_pince_commande(robot, 6, "STANDBY")

    set_pince_commande(robot, 1, "OUVERTURE")
    await robot.movement.async_angle_0(110, 4.7)  # Etape 1
    set_pince_commande(robot, 1, "FERMETURE")
    time.sleep(0.5)
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 /3)  # Etape 2
    set_pince_commande(robot, 2, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_120(110, 2)  # Etape 1
    set_pince_commande(robot, 2, "FERMETURE")
    time.sleep(0.5)
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 /6)  # Etape 2
    set_pince_commande(robot, 3, "OUVERTURE")
    await robot.movement.async_angle_240(110, 6)  # Etape 1
    set_pince_commande(robot, 3, "FERMETURE")
    time.sleep(0.5)
    await robot.movement.async_angle_300(110, 5)  # Etape 1
    await robot.movement.async_angle_0(110, 4.5)  # Etape 1

    set_pince_commande(robot, 1, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_180(110, 1.5)  # étape 10
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 / 3)  # étape 11
    await robot.movement.async_angle_120(110, 1)  # étape 12
    set_pince_commande(robot, 2, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_300(110, 1)  # étape 13
    await robot.movement.async_rotation_gauche(115, 9.45 / 2 / 3)  # étape 14
    await robot.movement.async_angle_60(110, 1)  # étape 15
    set_pince_commande(robot, 3, "OUVERTURE")
    time.sleep(0.5)
    await robot.movement.async_angle_180(110, 1)  # étape 13
    # time.sleep(18) # TODO Add to make robot wait for the other one

    await robot.movement.async_angle_120(110, 4.2)  # étape 13




async def run(robot: Robot):
    robot.arduino.send("R1+get_team")
    time.sleep(0.2)

    if robot.team == "bleu":
        await strat_bleu(robot)
    elif robot.team == "vert":
        await strat_vert(robot)
    else:
        set_pince_commande(robot, 1, "STANDBY")
        set_pince_commande(robot, 2, "STANDBY")
        set_pince_commande(robot, 3, "STANDBY")
        set_pince_commande(robot, 4, "STANDBY")
        set_pince_commande(robot, 5, "STANDBY")
        set_pince_commande(robot, 6, "STANDBY")
