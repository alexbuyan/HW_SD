from src.parser import Parser
from src.interpreter import Interpreter


class ParseManager:
    def __init__(self):
        """
        ParseManager constructor creates Parser and Interpreter
        """
        self.__parser = Parser()
        self.__interpreter = Interpreter()

    def process_input(self, input_str: str) -> str:
        """
        Parses given input_str into AST using Parser
        Checks the structure of AST
        Returns the result of input execution
        :param input_str: str
        :return: str
        """
        ast = self.__parser.parse(input_str)
        self.__interpreter.checkAST(ast)
        return self.__interpreter.evaluate(ast)
