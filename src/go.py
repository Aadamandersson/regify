#!/usr/bin/env python3
import sys
from lexer import Lexer, Token
from parser import Parser
import re
import difflib
        
def read_file(fn):
    src = ""
    with open(fn, "r") as f:
        src = f.read()
    return src

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Expected argument: {} <filename>".format(sys.argv[0]))
        sys.exit(1)

    source_code = ""
    with open(sys.argv[1], "r") as f:
        source_code = f.read()
    print("SOURCE CODE:\n{}".format(source_code))
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    expr = parser.parse()
    pattern = ""
    for e in expr:
        pattern += e.evaluate()

    print("RESULT:\n{}".format(pattern))






