import logging
import threading

from tactisoft.cli import NonBlockingCLI
from tactisoft.threadedserial import ThreadedSerial


class SharedRobot:
    match_started = threading.Event()  # Event set when match

    def __init__(self, name):
        self.name = name
        self.arduino = ThreadedSerial("/dev/arduino", 9600, on_message=self.on_arduino_message, raw=False, prefix="R2+")

    def on_arduino_message(self, message) -> bool:
        logging.debug("Arduino -> Robot: " + message)
        if message.startswith("START"):
            self.match_started.set()  # Set the event to start the match
        else:
            return False  # If not handled, return false

        return True  # If handled, return true

    def register_commands(self, cli: NonBlockingCLI):
        cli.register_command("arduino_raw", lambda x: self.arduino.send(x), "Send a raw command to the arduino", "arduino_raw <command>")
