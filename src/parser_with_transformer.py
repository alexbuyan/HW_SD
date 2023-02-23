import os
import sys
from typing import List

from lark import Lark, ast_utils, Transformer, v_args
from dataclasses import dataclass

this_module = sys.modules[__name__]

grammar = """
start: pipeline

pipeline: cmd
pipe: /\|/

cmd: cmd_name (sep args)*
cmd_name: /(cat|echo|wc|pwd|exit)/

args: arg sep args
    | arg
arg: /[^\|\s]+/

sep: /\s+/
"""

class MyTransformer(Transformer):
    def sep(self, data):
        return data[0].value

    def cmd_name(self, data):
        return data[0].value

    def arg(self, data):
        return data[0].value

    def pipe(self, data):
        return '|'

    def args(self, data):
        arguments = ''.join(data)
        return arguments

    def cmd(self, data):
        cmd_name, sep, arguments = data
        return (cmd_name, arguments)

    def pipeline(self, data):
        return data[0]

    def start(self, data):
        return data[0]


parser = Lark(grammar, start='start', parser='lalr')


def parse(text):
    tree = parser.parse(text)
    print(MyTransformer().transform(tree))

if __name__ == "__main__":
    parse("wc -l src tests")
