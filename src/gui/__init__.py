import signal
import sys

from src.parse_manager import ParseManager


class GUI:
    def __init__(self):
        self.__parse_manager = ParseManager()

    def run(self):
        signal.signal(signal.SIGINT, self.exit)
        while True:
            input_str = input('cli> ')
            self.__parse_manager.process_input(input_str)

    def exit(self, signal, frame):
        sys.exit(0)
