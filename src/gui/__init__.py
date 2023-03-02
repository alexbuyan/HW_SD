import signal
import sys

from src.parse_manager import ParseManager


class GUI:
    def __init__(self):
        self.__parse_manager = ParseManager()

    def run(self):
        """
        Reads inputs and outputs results processed by ParseManager function process_input
        :return: None
        """
        signal.signal(signal.SIGINT, self.exit)
        while True:
            input_str = input('cli> ')
            result = self.__parse_manager.process_input(input_str)
            if result:
                print(result)

    def exit(self, signal, frame):
        sys.exit(0)
