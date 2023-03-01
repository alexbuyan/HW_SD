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
        res1 = self.evaluate(cmd1)
        if not cmd2:
            return res1  # if this was not pipeline and just one command
        name2 = cmd2.name
        args2 = cmd2.args.values
        args2.append(res1)
        cmd2 = Cmd(name=name2, args=Args(args2))
        res2 = self.evaluate(cmd2)
        stream = os.popen(f"{res2}")  # doesn't work like this ????
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
