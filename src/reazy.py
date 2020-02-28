#!/usr/bin/env python3
import sys
from lexer import Lexer, Token
from parser import Parser
import re
import difflib

def generate(input):
    lexer = Lexer(input)
    parser = Parser(lexer)
    expr = parser.parse()
    pattern = ""
    for e in expr:
        pattern += e.evaluate()
    return pattern

def generate_from_file(path):
    src = ""
    with open(path, "r") as f:
        src = f.read()
    return generate(src)
