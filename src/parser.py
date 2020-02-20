#!/usr/bin/env python3
import sys
from token import Token
from ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr_token = 0
        self.tok_idx = -1
        self.get_next_token() 
        self.curr_ident = ""
    
    def get_next_token(self):
        self.prev_token = self.curr_token
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.curr_token = self.tokens[self.tok_idx]
        return self.curr_token
    
    def expect(self, tok_typ):
        if self.curr_token[0] is not tok_typ:
            print("Syntax error: expected {} found {} in {}\n".format(
                tok_typ, self.curr_token[0], self.curr_ident))
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
        self.get_next_token() 
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.NUM.name)
        self.get_next_token() 
        arg2 = None
        if self.curr_token[1] in ["varchar", "VARCHAR"]:
            self.curr_ident = "VARCHAR"
            arg2 = self.parse_varchar()
        elif self.curr_token[1] in ["text", "TEXT"]:
            self.curr_ident = "TEXT"
            arg2 = self.parse_text()
        else:
            # syntax error
            arg2 = self.curr_token[1]
        if (self.accept(Token.R_PAREN.name)):
            return NRepeat(arg1, arg2)
    
    def parse_any(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        children = []
        ret = None
        while self.accept(Token.COMMA.name) or self.curr_token[0] is Token.IDENT.name:
            if self.curr_token[1] in ["varchar", "VARCHAR"]:
                self.curr_ident = "VARCHAR"
                children.append(self.parse_varchar())
            elif self.curr_token[1] in ["text", "TEXT"]:
                self.curr_ident = "TEXT"
                children.append(self.parse_text())
            elif self.curr_token[1] in ["repeat", "REPEAT"]:
                self.curr_ident = "REPEAT"
                children.append(self.parse_repeat())
        ret = NAny(children)
        self.expect(Token.R_PAREN.name)
        return ret

    def parse_capture_group(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        capture = []
        ret = None
        while self.accept(Token.COMMA.name) or self.curr_token[0] is Token.IDENT.name:
            if self.curr_token[1] in ["varchar", "VARCHAR"]:
                self.curr_ident = "VARCHAR"
                capture.append(self.parse_varchar())
            elif self.curr_token[1] in ["text", "TEXT"]:
                self.curr_ident = "TEXT"
                capture.append(self.parse_text())
            elif self.curr_token[1] in ["repeat", "REPEAT"]:
                self.curr_ident = "REPEAT"
                capture.append(self.parse_repeat())
            elif self.curr_token[1] in ["any", "ANY"]:
                self.curr_ident = "ANY"
                capture.append(self.parse_any())
        ret = NCaptureGroup(capture)
        self.expect(Token.R_PAREN.name)
        return ret


    def parse(self):
        expr = []
        while self.tok_idx < len(self.tokens):
            if self.curr_token[0] is Token.IDENT.name:
                if self.curr_token[1] in ["varchar", "VARCHAR"]:
                    expr.append(self.parse_varchar())
                elif self.curr_token[1] in ["text", "TEXT"]:
                    expr.append(self.parse_text())
                elif self.curr_token[1] in ["repeat", "REPEAT"]:
                    expr.append(self.parse_repeat())
                elif self.curr_token[1] in ["any", "ANY"]:
                    expr.append(self.parse_any())
                elif self.curr_token[1] in ["group", "GROUP"]:
                    expr.append(self.parse_capture_group())
            else:
                self.get_next_token()
        return expr


