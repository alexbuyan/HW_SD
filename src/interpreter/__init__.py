import os
from src.cli_ast import Cmd, Args, Pipeline, EnvCall, EnvInit
from multipledispatch import dispatch


class Interpreter:
    def __init__(self):
        self.__env_variables = dict()

    def __add_env_var(self, name, value):
        self.__env_variables[name] = value

    def __get_env_var(self, name):
        return self.__env_variables.get(name)

    def checkAST(self, ast):
        print(f'interpreter got ast : {ast}')

    @dispatch(str)
    def evaluate(self, node):
        return node

    @dispatch(Pipeline)
    def evaluate(self, pipeline):
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
        stream = os.popen(f"{executed_command}")
        result = stream.read()
        stream.close()
        return result

    @dispatch(Cmd)
    def evaluate(self, cmd):
        name = cmd.name
        args = cmd.args
        transformed_args = self.evaluate(args)
        if name == "exit":
            exit()
        stream = os.popen(f"{name} {transformed_args}")  # might freeze ????
        result = stream.read()
        stream.close()
        return result

    @dispatch(Args)
    def evaluate(self, args):
        transformed_args = []
        for arg in args.values:
            transformed_args.append(self.evaluate(arg))
        return ' '.join(transformed_args)

    @dispatch(EnvCall)
    def evaluate(self, env_call):
        name = env_call.name
        value = self.__get_env_var(name)
        return value

    @dispatch(EnvInit)
    def evaluate(self, env_init):
        name = env_init.name
        value = env_init.value
        self.__add_env_var(name, value)
