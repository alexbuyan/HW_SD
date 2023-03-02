from lark import UnexpectedInput

from src.exceptions import InterpreterEvaluationException
from src.parser import Parser
from src.interpreter import Interpreter


class ParseManager:
    def __init__(self):
        self.__parser = Parser()
        self.__interpreter = Interpreter()

    def process_input(self, input_str: str) -> str:
        try:
            ast = self.__parser.parse(input_str)
            self.__interpreter.check_Ast(ast)
            return self.__interpreter.evaluate(ast)
        except UnexpectedInput as e:
            return e.get_context(input_str)
        except InterpreterEvaluationException as e:
            return e.get_message()
