from src.parser import Parser
from src.interpreter import Interpreter


class ParseManager:
    def __init__(self):
        self.__parser = Parser()
        self.__interpreter = Interpreter()

    def process_input(self, input_str: str):
        ast = self.__parser.parse(input_str)
        self.__interpreter.execute(ast)
