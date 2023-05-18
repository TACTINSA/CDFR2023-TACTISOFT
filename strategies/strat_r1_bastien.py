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

# avance jusqu'à la pile maron avec la pince ouverte ( notre second robot doit être en pause )
# marque un arrêt et ferme la pince, attends une demi seconde avant de reprendre le chemin

    set_pince_commande(robot, 1, "OUVERTURE")
    robot.movement.angle_0(110)
    time.sleep(8)
    robot.movement.stop()
    set_pince_commande(robot, 1, "FERMETURE")
    time.sleep(0.5)

# fait marche arrière jusqu'à la case verte avec un 90° vers la gauche, marche avant, 90° vers la gauche, 30°
# robot.movement.rotation_droite(115) #9.67 sec pour 2 tours sur lui même quasi parfait

    robot.movement.angle_180(110)
    time.sleep(7)
    robot.movement.stop()
    robot.movement.rotation_gauche(115)
    time.sleep(9.67/2/4)
    robot.movement.stop()
    time.sleep(0.5)
    robot.movement.angle_0(110)
    time.sleep(4)
    robot.movement.stop()
    time.sleep(0.5)
    robot.movement.rotation_gauche(115)
    time.sleep(9.67/2/12)
    robot.movement.stop()
    time.sleep(0.5)

# ouvre la pince et avance, la referme, fait une rotation, ouvre la pince et avance, la referme, fait marche arrièce

    set_pince_commande(robot, 2, "OUVERTURE")
    time.sleep(0.5)
    robot.movement.angle_120(110)
    time.sleep(3)
    robot.movement.stop()
    set_pince_commande(robot, 2, "FERMETURE")
    time.sleep(0.5)
    robot.movement.rotation_gauche(115)
    time.sleep(9.67/2/3)
    robot.movement.stop()
    time.sleep(0.5)
    set_pince_commande(robot, 3, "OUVERTURE")
    time.sleep(0.5)
    robot.movement.angle_240(110)
    time.sleep(4)
    robot.movement.stop()
    set_pince_commande(robot, 6, "FERMETURE")
    robot.movement.stop()
    time.sleep(1.5)
    robot.movement.angle_60(110)
    time.sleep(1.5)
    set_pince_commande(robot, 3, "STANDBY")
    robot.movement.rotation_gauche(115)
    time.sleep(9.67/2/2)
    set_pince_commande(robot, 1, "OUVERTURE")
    robot.movement.angle_0(110)
    time.sleep(1)
    robot.movement.stop()
    set_pince_commande(robot, 4, "FERMETURE")
    time.sleep(1)
    robot.movement.angle_180(110)
    set_pince_commande(robot, 1, "STANDBY")
    time.sleep(1)
    robot.movement.angle_120(110)
    set_pince_commande(robot, 2, "OUVERTURE")
    time.sleep(1)
    set_pince_commande(robot, 5, "FERMETURE")
    robot.movement.stop()
    time.sleep(0.5)


async def strat_vert(robot: Robot):
    set_pince_commande(robot, 1, "STANDBY")
    set_pince_commande(robot, 2, "STANDBY")
    set_pince_commande(robot, 3, "STANDBY")
    set_pince_commande(robot, 4, "STANDBY")
    set_pince_commande(robot, 5, "STANDBY")
    set_pince_commande(robot, 6, "STANDBY")

    time.sleep(2)

    set_pince_commande(robot, 1, "OUVERTURE")
    set_pince_commande(robot, 4, "FERMETURE")

    time.sleep(5)

    set_pince_commande(robot, 2, "OUVERTURE")
    set_pince_commande(robot, 5, "FERMETURE")

    time.sleep(5)

    set_pince_commande(robot, 3, "OUVERTURE")
    set_pince_commande(robot, 6, "FERMETURE")

    time.sleep(5)



async def run(robot: Robot):
    robot.arduino.send("R1+get_team")
    time.sleep(0.2)

    if robot.team == "bleu":
        await strat_bleu(robot)
    elif robot.team == "vert":
        await strat_vert(robot)
    else:
        logging.error("Invalid team")