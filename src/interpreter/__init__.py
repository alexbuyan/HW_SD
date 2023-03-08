import os
from src.cli_ast import Cmd, Args, Pipeline, EnvCall, EnvInit
from multipledispatch import dispatch

from src.exceptions import InterpreterEvaluationException


class Interpreter:
    def __init__(self):
        """
        Interpreter constructor creates dictionary to store environment variables
        """
        self.__env_variables = dict()

    def __add_env_var(self, name, value):
        """
        Adds environment variable into dictionary
        :param name:  str
        :param value: Any
        :return: None
        """
        self.__env_variables[name] = value

    def __get_env_var(self, name):
        """
        Returns environment variable by name
        :param name: str
        :return: Any
        """
        return self.__env_variables.get(name)

    def check_Ast(self, ast):
        """
        Prints the structure of AST
        :param ast: AST
        :return: None
        """
        print(f'interpreter got ast : {ast}')

    @dispatch(str)
    def evaluate(self, node):
        """
        If met string in AST return it
        :param node: str
        :return: str
        """
        return node

    @dispatch(Pipeline)
    def evaluate(self, pipeline):
        """
        Evaluates provided Pipeline from AST
        :param pipeline: Pipeline
        :return: str
        """
        commands = pipeline.commands
        if len(commands) == 1:
            return self.evaluate(commands[0])

        executed_command = ""
        for command in commands:
            if command == '|':
                executed_command += ' ' + command + ' '
            else:
                name = command.name
                args = self.evaluate(command.args)
                executed_command += name + ' ' + args

        try:
            stream = os.popen(f"{executed_command}")
        except Exception:
            raise InterpreterEvaluationException()

        result = stream.read()
        stream.close()
        return result

    @dispatch(Cmd)
    def evaluate(self, cmd):
        """
        Evaluates provided Cmd from AST
        :param cmd: Cmd
        :return: str
        """
        name = cmd.name
        args = cmd.args
        transformed_args = self.evaluate(args)
        if name == "exit":
            exit()

        try:
            stream = os.popen(f"{name} {transformed_args}")
        except Exception:
            raise InterpreterEvaluationException()

        result = stream.read()
        stream.close()
        return result

    @dispatch(Args)
    def evaluate(self, args):
        """
        Evaluates provided Args in AST
        :param args: Args
        :return:
        """
        transformed_args = []
        for arg in args.values:
            transformed_args.append(self.evaluate(arg))
        return ' '.join(transformed_args)

    @dispatch(EnvCall)
    def evaluate(self, env_call):
        """
        Evaluates provided call of environment variable in AST
        :param env_call: EnvCall
        :return: Any
        """
        name = env_call.name
        value = self.__get_env_var(name)
        return value

    @dispatch(EnvInit)
    def evaluate(self, env_init):
        """
        Initialize environment variable by adding it to dictionary
        :param env_init: EnvInit
        :return: None
        """
        name = env_init.name
        value = env_init.value
        self.__add_env_var(name, value)
