import sys
from dataclasses import dataclass
from typing import List

from lark import ast_utils, Transformer, v_args

module = sys.modules[__name__]


class _Ast(ast_utils.Ast):
    # This will be skipped by create_transformer(), because it starts with an underscore
    pass


@dataclass
class Args(_Ast, ast_utils.AsList):
    values: List


@dataclass
class Cmd(_Ast):
    name: str
    args: Args


@dataclass
class Pipeline(_Ast):
    cmd1: Cmd
    pipe: str = None
    cmd2: Cmd = None

@dataclass
class EnvInit:
    env_name: str
    env_value: str

@dataclass
class EnvsInit(_Ast, ast_utils.AsList):
    envs: List[EnvInit]

class AstTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.__env_context = dict()

    def cmd_name(self, data):
        # TODO FIX HERE
        print(data)
        return data

    def arg(self, data):
        return data[0].value

    def pipe(self, data):
        return '|'

    def env_name(self, data):
        return data[0].value

    def env_init(self, data):
        name, value = data
        self.__env_context[name] = value
        return EnvInit(name, value)

    @v_args(inline=True)
    def env(self, data):
        name = data
        value = self.__env_context.get(name)
        if not value:
            raise Exception("no such env var")
        return value

    @v_args(inline=True)
    def start(self, data):
        return data
