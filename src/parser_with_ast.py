import os
import sys
from typing import List

from lark import Lark, Transformer, ast_utils, v_args
from dataclasses import dataclass

this_module = sys.modules[__name__]

grammar = """
%import common.WS
%ignore WS

start: pipeline

pipeline: (cmd pipe)* cmd
pipe: /\|/

cmd: cmd_name args
cmd_name: /(cat|echo|wc|pwd|exit)/

args: arg*
arg: /\w+/
"""

# -- AST --
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

class MyTransformer(Transformer):
    def cmd_name(self, data):
        return data[0].value

    def arg(self, data):
        return data[0].value

    def pipe(self, data):
        return '|'

    @v_args(inline=True)
    def start(self, data):
        return data
# -- AST --

# -- Transformer (creates AST from parse_tree) --
transformer = ast_utils.create_transformer(this_module, MyTransformer())
# -- Transformer (creates AST from parse_tree) --

# -- Parser --
parser = Lark(grammar, start='start', parser='lalr')

def parse(text):
    tree = parser.parse(text)
    ast = transformer.transform(tree)
    return ast
# -- Parser --

# -- Interpreter --
def evaluate_arg(arg: str):
    return arg

def evaluate_args(args: Args):
    transformed_args = []
    for arg in args.values:
        transformed_args.append(evaluate(arg))
    return ' '.join(transformed_args)

def evaluate_cmd(cmd: Cmd):
    name = cmd.name 
    args = cmd.args
    tranformed_args = evaluate(args)
    stream = os.popen(f"{name} {tranformed_args}") #might freeze ????
    result = stream.read()
    stream.close()
    return result

def evaluate_pipeline(pipeline: Pipeline):
    cmd1 = pipeline.cmd1
    cmd2 = pipeline.cmd2
    pipe = pipeline.pipe
    res1 = evaluate(cmd1)
    if not cmd2:
        return res1 # if this was not pipeline and just one command
    res2 = evaluate(cmd2)
    stream = os.popen(f"{res2} {res1}") # doesn't work like this ????
    result = stream.read()
    stream.close()
    return result

def evaluate(node):
    if isinstance(node, Cmd):
        return evaluate_cmd(node)
    elif isinstance(node, Args):
        return evaluate_args(node)
    elif isinstance(node, Pipeline):
        return evaluate_pipeline(node)
    return evaluate_arg(node)

def interpreter(ast):
    return evaluate(ast)
# -- Interpreter --


if __name__ == "__main__":
    ast = parse("echo 123")
    result = evaluate(ast)
    print(result)
