import logging
import threading

from tacticom import TactiCom

from tactisoft.cli import NonBlockingCLI
from tactisoft.threadedserial import ThreadedSerial


class SharedRobot:
    match_started = threading.Event()  # Event set when match

    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix
        self.arduino = TactiCom(self.prefix, "/dev/arduino", 9600, self.on_command)
        self.score = 49  # TODO estimation

    def on_command(self, command: str, args: list):
        logging.debug("Arduino -> Robot: " + command + " with args: " + str(args))
        if command == "START":
            self.match_started.set()  # Set the event to start the match
        else:
            return False  # If not handled, return false

        return True  # If handled, return true

    def register_commands(self, cli: NonBlockingCLI):
        cli.register_command("arduino_raw", lambda x: self.arduino.send(x), "Send a raw command to the arduino", "arduino_raw <command>")
