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
    pass


async def strat_vert(robot: Robot):
    set_pince_commande(robot, 1, "OUVERTURE")
    set_pince_commande(robot, 2, "OUVERTURE")
    set_pince_commande(robot, 3, "OUVERTURE")
    time.sleep(1)
    set_pince_commande(robot, 1, "FERMETURE")
    set_pince_commande(robot, 2, "FERMETURE")
    set_pince_commande(robot, 3, "STANDBY")
    time.sleep(1)
    robot.movement.forward(100)
    time.sleep(5)
    robot.movement.stop()


async def run(robot: Robot):
    robot.arduino.send("R1+get_team")
    time.sleep(0.2)

    if robot.team == "bleu":
        await strat_bleu(robot)
    elif robot.team == "vert":
        await strat_vert(robot)
    else:
        logging.error("Invalid team")