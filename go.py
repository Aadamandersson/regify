#!/usr/bin/env python3
import sys
from lexer import Lexer

class NRange:
    def __init__(self, text, start, end=None):
        self.text = text
        self.start = start
        self.end = end

    def __str__(self):
        if self.start in ['*', '+']:
            return "[{0}]{{,}}".format(self.text)
        if self.end is None:
            return "[{0}]{{{1}}}".format(self.text, self.start)
        else:
            return "[{0}]{{{1},{2}}}".format(self.text, self.start, self.end)


class NText:
    def __init__(self, text, next_tok):
        self.text = text
        self.next_tok = next_tok
    def __str__(self):
        if self.next_tok == "range" and self.text == '[':
            return '\\' + self.text
        return self.text

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr_token = 0
        self.tok_idx = -1
        self.get_next_token() 
    
    def get_next_token(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.curr_token = self.tokens[self.tok_idx]
        return self.curr_token
    
    def expect(self, tok_typ):
        if self.curr_token[0] is not tok_typ:
            print("Syntax error: expected {} found {}\n".format(
                tok_typ, self.curr_token[0]))
            sys.exit(1)
        self.get_next_token()

    def accept(self, tok_typ):
        if self.curr_token[0] is not tok_typ:
            return False
        self.get_next_token()
        return True
    
    def parse(self):
        expr = []
        while self.tok_idx < len(self.tokens):
            if self.curr_token[0] is Token.IDENT.name:
                if self.curr_token[1] == "range":
                    self.get_next_token()
                    self.expect(Token.L_PAREN.name)
                    arg1 = self.curr_token[1]
                    self.expect(Token.STRING.name)
                    self.get_next_token()
                    arg2 = self.curr_token[1]
                    self.expect(Token.NUM.name)
                    if self.accept(Token.R_PAREN.name):
                        expr.append(NRange(arg1, arg2))
                    else:
                        self.get_next_token()
                        arg3 = self.curr_token[1]
                        self.expect(Token.NUM.name)
                        expr.append(NRange(arg1, arg2, arg3))
                elif self.curr_token[1] == "text":
                    self.get_next_token()
                    self.expect(Token.L_PAREN.name)
                    arg1 = self.curr_token[1]
                    self.expect(Token.STRING.name)
                    self.expect(Token.R_PAREN.name)
                    expr.append(NText(arg1, self.curr_token[1]))
            else:
                self.get_next_token()
        return expr



#grep -o '\[[A-Z][a-z]\{,\}->]'
#[range(“A-Z”,1)range(“a-z”, *)->]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Expected argument: {} <filename>".format(sys.argv[0]))
        sys.exit(1)

    source_code = ""
    with open(sys.argv[1], "r") as f:
        source_code = f.read()
    print("SOURCE: {}".format(source_code))
    print("RESULT:")
    lexer = Lexer(source_code)
    parser = Parser(lexer.lex())
    expr = parser.parse()

    for e in expr:
        print(e, end='')
    print()








