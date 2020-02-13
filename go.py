#!/usr/bin/env python3
import sys
from lexer import Lexer, Token
import re
import difflib

class NVarChar:
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

    def __new__(self, text, start, end=None):
        if start in ['*', '+']:
            return "[{0}]{{,}}".format(text)
        if end is None:
            return "[{0}]{{{1}}}".format(text, start)
        else:
            return "[{0}]{{{1},{2}}}".format(text, start, end)

class NText:
    def __init__(self, text, next_tok):
        self.text = text
        self.next_tok = next_tok

    def __str__(self):
        if self.next_tok == "varchar" and self.text == '[':
            return '\\' + self.text
        return self.text
    def __new__(self, text, next_tok):
        if next_tok == "varchar" and text == '[':
            return '\\' + text
        return text

class NRepeat:
    def __init__(self, num, child):
        self.num = num
        self.child = child
    def __str__(self):
        ret = ""
        for i in range(0, self.num):
            ret += child
        return ret
    def __new__(self, num, child):
        ret = ""
        for i in range(0, int(num)):
            ret += child
        return ret

class NAny:
    def __init__(self, *args):
        pass
        
    def __str__(self):
        ret = ""
        for i in range(0, len(args)):
            ret += args[i] + "|"
        return ret

    def __new__(self, *args):
        ret = ""
        for i in range(0, len(args)):
            ret += args[i] + "|"

        return ret

        
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

    def parse_varchar(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.STRING.name)
        self.get_next_token()
        arg2 = self.curr_token[1]
        self.expect(Token.NUM.name)
        if self.accept(Token.R_PAREN.name):
            return NVarChar(arg1, arg2)
        else:
            self.get_next_token()
            arg3 = self.curr_token[1]
            self.expect(Token.NUM.name)
            return NVarChar(arg1, arg2, arg3)

    def parse_text(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.STRING.name)
        self.expect(Token.R_PAREN.name)
        return NText(arg1, self.curr_token[1])

    def parse_repeat(self):
        self.get_next_token()  # eat 'repeat'
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.NUM.name)
        self.get_next_token() # ','
        arg2 = None
        if (self.curr_token[1] == "varchar"):
            arg2 = self.parse_varchar()
        elif (self.curr_token[1] == "text"):
            arg2 = self.parse_text()
        else:
            # syntax error
            arg2 = self.curr_token[1]
        if (self.accept(Token.R_PAREN.name)):
            return NRepeat(arg1, arg2)

    def parse(self):
        expr = []
        while self.tok_idx < len(self.tokens):
            if self.curr_token[0] is Token.IDENT.name:
                if self.curr_token[1] == "varchar":
                    expr.append(self.parse_varchar())
                elif self.curr_token[1] == "text":
                    expr.append(self.parse_text())
                elif self.curr_token[1] == "repeat":
                    expr.append(self.parse_repeat())
                elif self.curr_token[1] == "any":
                    self.get_next_token()
                    self.expect(Token.L_PAREN.name)
                while self.accept(Token.COMMA.name) or self.curr_token[0] is Token.IDENT.name:
                    if (self.curr_token[1] == "varchar"):
                        expr.append(NAny(self.parse_varchar()))
                    elif (self.curr_token[1] == "text"):
                        expr.append(NAny(self.parse_text()))
                    elif (self.curr_token[1] == "repeat"):
                        expr.append(NAny(self.parse_repeat()))

                self.expect(Token.R_PAREN.name)

            else:
                self.get_next_token()
        return expr



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
    print("SOURCE:\n{}".format(source_code))
    lexer = Lexer(source_code)
    parser = Parser(lexer.lex())
    expr = parser.parse()
    pattern = ""
    for e in expr:
        pattern += e
    print("RESULT:\n{}".format(pattern))
    m = re.findall(pattern, read_file("datasets/q4data.txt"))
    res = ""
    for r in m:
        res += r + '\n'

    d = difflib.Differ()
    diff = difflib.unified_diff([read_file("datasets/q4hits.txt")], [res], lineterm='')
    if '\n'.join(diff) is not '':
        print("MATCH FAILED:\n\n{}".format('\n'.join(diff)))
    else:
        print("SUCCESSFULLY MATCHED")






