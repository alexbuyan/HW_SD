from lark import ast_utils, Lark, UnexpectedInput
from src.cli_ast import module, AstTransformer
from src.lexer import grammar


class Parser:
    def __init__(self):
        self.__transformer = ast_utils.create_transformer(module, AstTransformer())
        self.__parser = Lark(grammar, start='start', parser='lalr')

    def parse(self, input_str: str):
        try:
            parse_tree = self.__parser.parse(input_str)
            ast = self.__transformer.transform(parse_tree)
            return ast
        except UnexpectedInput:
            raise
