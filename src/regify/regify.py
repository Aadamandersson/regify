from .parser.lexer import Lexer
from .parser.parser import Parser


def generate(source_code):
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()
    pattern = ""
    for node in ast:
        pattern += node.evaluate()
    return pattern

def generate_from_file(path):
    source_code = ""
    with open(path, "r") as f:
        source_code = f.read()
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()
    pattern = ""
    for node in ast:
        pattern += node.evaluate()
    return pattern