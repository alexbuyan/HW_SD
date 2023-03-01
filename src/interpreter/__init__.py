import os
import sys
from dataclasses import dataclass
from typing import List
from src import cli_ast
from src.cli_ast import Cmd, Args, Pipeline


class Interpreter:
    def execute(self, ast):
        print(f'interpreter got ast : {ast}')

    def evaluate(self, node):
        if isinstance(node, Cmd):
            return self.evaluate_cmd(node)
        elif isinstance(node, Args):
            return self.evaluate_args(node)
        elif isinstance(node, Pipeline):
            return self.evaluate_pipeline(node)
        return self.evaluate_arg(node)

    def evaluate_cmd(self, cmd: Cmd):
        name = cmd.name
        args = cmd.args
        transformed_args = self.evaluate(args)
        stream = os.popen(f"{name} {transformed_args}")  # might freeze ????
        result = stream.read()
        stream.close()
        return result

    def evaluate_args(self, args: Args):
        transformed_args = []
        for arg in args.values:
            transformed_args.append(self.evaluate(arg))
        return ' '.join(transformed_args)

    def evaluate_pipeline(self, pipeline: Pipeline):
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

    def evaluate_arg(self, arg: str):
        return arg
