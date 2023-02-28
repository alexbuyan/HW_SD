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


class AstTransformer(Transformer):
    def cmd_name(self, data):
        return data[0].value

    def arg(self, data):
        return data[0].value

    def pipe(self, data):
        return '|'

    @v_args(inline=True)
    def start(self, data):
        return data
