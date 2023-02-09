#!/usr/bin/env python3

import argparse
import logging
from time import sleep

from robot.robot import Robot
from robot.robot2 import Robot2
from tactisoft.cli import NonBlockingCLI
import tactisoft.server as server

should_stop = False
cli = None
robot = None


def set_stop(_should_stop):
    global should_stop
    should_stop = _should_stop


def launch_strategy(_strategy, _robot):
    getattr(__import__("strategies.%s" % _strategy, fromlist=["run"]), "run")(_robot)


if __name__ == '__main__':
    # All options that can be passed as parameter are defined here
    parser = argparse.ArgumentParser(description='TACTISOFT v2.0 - CDR 2023 - TACTINSA')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--strategy', help='Run the strategy with the given name')
    group.add_argument('--cli', action='store_true', help='Provide control commands in console')
    group.add_argument('--server', action='store_true', help='Provide remote control')
    parser.add_argument('--no-collision', action='store_true', help='Disable all collisions detection')
    parser.add_argument('--no-startup', action='store_true', help='Bypass the startup process')
    parser.add_argument('--log-level', choices=["debug", "info", "warning", "error", "critical"], help='Set the logging level', default="info")
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

    import tactisoft.line_following
    if not args.no_startup:
        logging.info("Waiting for match start")
        robot.match_started.wait()
    else:
        robot.match_started.set()

    if args.strategy:  # Run the strategy
        # launch the run(robot: Robot) function from the python file in strategies folder with args.strategy as name
        launch_strategy(args.strategy, robot)
    elif args.cli or args.server:  # or start the CLI and/or the server
        cli = NonBlockingCLI()  # Init the cli for the robot to register commands
        robot.register_commands(cli)
        cli.register_command("exit", lambda: set_stop(True), "Exit the program", "exit")
        cli.register_command("strategy", lambda x: launch_strategy(x, robot), "Exit the program", "exit")

        if args.cli:  # Start processing the cli commands in the terminal
            cli.start()
            while not should_stop:
                sleep(0.1)
            cli.stop()

        if args.server:  # Start the server
            server.run_forever(cli)
