from lark import ast_utils, Lark
from src.cli_ast import module, AstTransformer
from src.lexer import grammar


class Parser:
    def __init__(self):
        """
        Parser constructor creates Transformer using ast_utils and parser using Lark
        """
        self.__transformer = ast_utils.create_transformer(module, AstTransformer())
        self.__parser = Lark(grammar, start='start', parser='lalr')

    def parse(self, input_str: str):
        """
        Parses input_str and transforms it into AST
        :param input_str: str
        :return: AST
        """
        parse_tree = self.__parser.parse(input_str)
        ast = self.__transformer.transform(parse_tree)
        return ast
