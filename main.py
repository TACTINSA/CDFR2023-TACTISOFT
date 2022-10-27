import argparse
import logging
from time import sleep

from robot.robot import Robot
from tactisoft import motors
from tactisoft.motors import Direction

if __name__ == '__main__':
    # All options that can be passed as parameter are defined here
    parser = argparse.ArgumentParser(description='TACTISOFT v2.0 - CDR 2023 - TACTINSA')
    parser.add_argument('--strategy', help='Run the strategy with the given name')
    parser.add_argument('--cli', action='store_true', help='Provide control commands in console')
    parser.add_argument('--server', action='store_true', help='Provide remote control')
    parser.add_argument('--no-collision', action='store_true', help='Disable all collisions detection')
    parser.add_argument('--no-startup', action='store_true', help='Bypass the startup process')
    parser.add_argument('--log-level', choices=["debug", "info", "warning", "error", "critical"], help='Set the logging level')
    args = parser.parse_args()

    # Set the logging level from the argparse argument
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level.upper())
    logging.basicConfig(level=numeric_level)

    logging.debug(args)

    # Init robot
    robot = Robot()

    sleep(1)  # Wait for the robot to be fully initialized before continuing
    robot.arduino.send("R2+INIT")
    logging.info("%s is initialized" % robot.name)

    if not args.no_startup:
        logging.info("Waiting for match start")
        robot.match_started.wait()
    else:
        robot.match_started.set()