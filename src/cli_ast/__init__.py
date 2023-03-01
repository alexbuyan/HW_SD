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
class Pipeline(_Ast, ast_utils.AsList):
    commands: List

@dataclass
class EnvInit(_Ast):
    name: str
    value: str


@dataclass
class EnvCall(_Ast):
    name: str


class AstTransformer(Transformer):
    def cmd_name(self, data):
        return data[0].value

    def val(self, data):
        value = data[0].value
        if value[0] == '"':
            value = value[1:-1]
        if value[0] == '$':
            return EnvCall(value[1:])
        return value

    def pipe(self, data):
        return '|'

    def env_name(self, data):
        return data[0].value

    @v_args(inline=True)
    def start(self, data):
        return data
