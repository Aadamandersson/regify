#!/usr/bin/env python3
import sys
from token import Token
from ast import *
from error import Error

class Parser:
    def __init__(self, lexer):
        self.tokens = lexer.lex()
        self.source_code = lexer.source_code
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
            print(Error(tok_typ, self.curr_token[1], self.curr_ident, self.curr_token[2], self.curr_token[3], self.source_code))
            sys.exit(1)
        self.get_next_token()

    def accept(self, tok_typ):
        if self.curr_token[0] is not tok_typ:
            return False
        self.get_next_token()
        return True

    def peek(self):
        if self.tok_idx + 1 < len(self.tokens):
            return self.tokens[self.tok_idx + 1]
        return self.tokens[self.tok_idx]

    def parse_varchar(self):
        self.curr_ident = "VARCHAR"
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.STRING.name)
        self.get_next_token()
        arg2 = self.curr_token[1]
        if self.accept(Token.NUM.name) or self.accept(Token.REP.name):
            if self.accept(Token.R_PAREN.name):
                return AstVarChar(arg1, arg2)
            else:
                self.get_next_token()
                arg3 = self.curr_token[1]
                self.expect(Token.NUM.name)
                if self.peek()[0] is Token.NUM.name:
                    e = Error(2, 3, self.curr_ident, self.curr_token[2], self.curr_token[3], self.source_code)
                    e.invalid_nr_of_args()
                else:
                    return AstVarChar(arg1, arg2, arg3)

        #Should be num or rep..
        self.expect(Token.NUM.name)

    """
    def parse_text(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.STRING.name)
        self.expect(Token.R_PAREN.name)
        return AstText(arg1, self.curr_token[1])
    """
    def parse_text(self):
        self.get_next_token()
        arg1 = self.curr_token[1]
        self.expect(Token.STRING.name)
        return AstText(arg1, self.curr_token[1])

    def parse_repeat(self):
        self.get_next_token() 
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.NUM.name)
        self.get_next_token() 
        children = []
        ret = None
        while self.accept(Token.COMMA.name) or self.curr_token[0] is Token.IDENT.name:
            if self.curr_token[1] in ["varchar", "VARCHAR"]:
                self.curr_ident = "VARCHAR"
                children.append(self.parse_varchar())
            elif self.curr_token[1] in ["any", "ANY"]:
                self.curr_ident = "ANY"
                children.append(self.parse_any())
            elif self.curr_token[1] is "@":
                self.curr_ident = "@"
                children.append(self.parse_text())
            
        ret = AstRepeat(arg1, children) 
        self.expect(Token.R_PAREN.name)
        return ret
    
    def parse_any(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        children = []
        ret = None
        while self.accept(Token.COMMA.name) or self.curr_token[0] is Token.IDENT.name:
            if self.curr_token[1] in ["varchar", "VARCHAR"]:
                self.curr_ident = "VARCHAR"
                children.append(self.parse_varchar())
            elif self.curr_token[1] is "@":
                self.curr_ident = "@"
                children.append(self.parse_text())
            elif self.curr_token[1] in ["repeat", "REPEAT"]:
                self.curr_ident = "REPEAT"
                children.append(self.parse_repeat())

        ret = AstAny(children)
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
            elif self.curr_token[1] is "@":
                self.curr_ident = "@"
                capture.append(self.parse_text())
            elif self.curr_token[1] in ["repeat", "REPEAT"]:
                self.curr_ident = "REPEAT"
                capture.append(self.parse_repeat())
            elif self.curr_token[1] in ["any", "ANY"]:
                self.curr_ident = "ANY"
                capture.append(self.parse_any())

        ret = AstCaptureGroup(capture)
        self.expect(Token.R_PAREN.name)
        return ret


    def parse(self):
        expr = []
        while self.tok_idx < len(self.tokens):
            if self.curr_token[0] is Token.IDENT.name:
                if self.curr_token[1] in ["varchar", "VARCHAR"]:
                    expr.append(self.parse_varchar())
                elif self.curr_token[1] is "@":
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


