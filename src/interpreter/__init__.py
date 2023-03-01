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
        cmd1 = pipeline.cmd1
        cmd2 = pipeline.cmd2
        pipe = pipeline.pipe
        if not cmd2:
            return self.evaluate(cmd1)
        name1 = cmd1.name
        args1 = cmd1.args
        args1 = self.evaluate(args1)
        name2 = cmd2.name
        args2 = cmd2.args
        args2 = self.evaluate(args2)
        stream = os.popen(f"{name1} {args1} {pipe} {name2} {args2}")
        result = stream.read()
        stream.close()
        return result

    @dispatch(Cmd)
    def evaluate(self, cmd):
        name = cmd.name
        args = cmd.args
        transformed_args = self.evaluate(args)
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
        if not value:
            # TODO raise no such env exception
            return
        return value

    @dispatch(EnvInit)
    def evaluate(self, env_init):
        name = env_init.name
        value = env_init.value
        self.__add_env_var(name, value)
