import logging
import threading
from time import sleep


class NonBlockingCLI:

    def __init__(self, prompt='CLI> '):
        self.prompt = prompt
        self.commands = {}
        self.running = False
        self.thread = None
        self.register_command('help', lambda x=None: self.help(x), 'Show this help', 'help [command]', 0)

    def help(self, command=None):
        if command is None:
            logging.info("List of commands:")
            for command in self.commands:
                logging.info("\t%s: %s" % (command, self.commands[command]['help']))
        else:
            if command in self.commands:
                logging.info("Help for command %s:" % command)
                logging.info("\t%s: %s" % (command, self.commands[command]['help']))
                logging.info("\tUsage: %s" % self.commands[command]['usage'])
            else:
                logging.info("Unknown command: %s" % command)

    def register_command(self, command, callback, help_text, usage, nb_args=None):
        self.commands[command] = {'callback': callback, 'help': help_text, 'usage': usage, 'nb_args': nb_args if nb_args is not None else callback.__code__.co_argcount}

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            command = input(self.prompt)
            command = command.split(' ')
            if command[0].lower() in self.commands:
                if len(command) - 1 >= self.commands[command[0]]['nb_args']:
                    self.commands[command[0]]['callback'](*command[1:])
                else:
                    logging.info("Invalid number of arguments. Got %d, expected %d" % (len(command) - 1, self.commands[command[0]]['nb_args']))
            else:
                logging.info("Unknown command: %s" % command)
            sleep(0.1)
