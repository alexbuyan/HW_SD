import sys
from typing import List

from lark import Lark, Transformer, ast_utils, v_args
from dataclasses import dataclass

this_module = sys.modules[__name__]

grammar = """
start: cmd

cmd: cmd_name args
cmd_name: /(cat|echo|wc|pwd|exit)/

args: (" " arg)+ 
arg: /\S+/
"""


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


class MyTransformer(Transformer):
    def cmd_name(self, data):
        return data[0].value

    def arg(self, data):
        return data[0].value

    def sep(self, data):
        pass

    def pipe(self, data):
        return '|'

    @v_args(inline=True)
    def start(self, data):
        return data


parser = Lark(grammar, start='cmd', parser='lalr')
transformer = ast_utils.create_transformer(this_module, MyTransformer())

def parse(text):
    tree = parser.parse(text)
    node = transformer.transform(tree)
    print(node)


if __name__ == "__main__":
    parse("wc -l src test")
