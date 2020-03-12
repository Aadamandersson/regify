#!/usr/bin/env python3
import sys
from .token import Token
from .ast import *
from .error import Error

class Parser:
    def __init__(self, lexer):
        self.tokens = lexer.lex()
        self.source_code = lexer.source_code
        self.curr_token = 0
        self.prev_token = self.curr_token
        self.tok_idx = -1
        self.curr_ident = ""
        self.get_next_token()

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

    def peek_nth(self, n):
        if self.tok_idx + n < len(self.tokens):
            return self.tokens[self.tok_idx + n]

    def parse_args(self, caller):
        children = []
        while self.accept(Token.COMMA.name) or self.curr_token[0] in [Token.IDENT.name, Token.KEYWORD.name]:
            _type = self.curr_token[1]
            if _type == "VARCHAR":
                self.curr_ident = _type
                children.append(self.parse_varchar())
            elif _type == "@":
                self.curr_ident = self.curr_token[1]
                children.append(self.parse_text())
            elif _type == "REPEAT" and _type != caller:
                self.curr_ident = _type
                children.append(self.parse_repeat())
            elif _type == "ANY" and _type != caller:
                self.curr_ident = _type
                children.append(self.parse_any())
            elif _type == "GROUP":
                self.curr_ident = _type
                children.append(self.parse_capture_group())
            elif _type == "INLINE" and _type != caller:
                self.curr_ident = _type
                self.get_next_token()
                children.append(self.parse_text())
            elif _type in ["OR", "START", "END"] and caller not in ["OR", "START", "END"]:
                self.curr_ident = _type
                children.append(self.parse_keyword(_type))
            else:
                e = Error("", self.curr_token[1], caller, self.curr_token[2], self.curr_token[3], self.source_code)
                e.unexpected_argument()

        return children

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
                if arg3 == "MORE":
                    self.get_next_token()
                    self.expect(Token.R_PAREN.name)
                    return AstVarChar(arg1, arg2, "")
                elif self.accept(Token.NUM.name):
                    if self.peek()[0] is Token.NUM.name:
                        e = Error(2, 3, self.curr_ident, self.curr_token[2], self.curr_token[3], self.source_code)
                        e.invalid_nr_of_args()
                    else:
                        self.expect(Token.R_PAREN.name)
                        return AstVarChar(arg1, arg2, arg3)
                else:
                    e = Error("", self.curr_token[1], arg3, self.curr_token[2], self.curr_token[3], self.source_code)
                    e.unexpected_argument()

        #Should be num or rep..
        self.expect(Token.NUM.name)

    """
    Old v
    def parse_text(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.STRING.name)
        self.expect(Token.R_PAREN.name)
        return AstText(arg1, self.curr_token[1])
    """

    def parse_text(self):
        prev_ident = ""
        try:
            prev_ident = self.prev_token[1]
        except:
            pass

        self.get_next_token()
        arg1 = self.curr_token[1]
        self.expect(Token.STRING.name)
        return AstText(arg1, prev_ident, self.curr_token[1])

    def parse_repeat(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)
        arg1 = self.curr_token[1]
        self.expect(Token.NUM.name)
        self.get_next_token()

        children = self.parse_args("REPEAT")
        ret = AstRepeat(arg1, children)
        self.expect(Token.R_PAREN.name)
        return ret

    def parse_any(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)

        children = self.parse_args("ANY")
        ret = AstAny(children)
        self.expect(Token.R_PAREN.name)
        return ret

    def parse_capture_group(self):
        self.get_next_token()
        self.expect(Token.L_PAREN.name)

        children = self.parse_args("GROUP")
        ret = AstNonCaptureGroup(children)
        self.expect(Token.R_PAREN.name)
        return ret

    def parse_keyword(self, _type):
        ret = AstKeyword(_type)
        self.expect(Token.KEYWORD.name)
        return ret


    def parse(self):
        expr = []

        while self.curr_token[0] != Token.EOF.name:
            if self.curr_token[0] == Token.IDENT.name:
                _type = self.curr_token[1]
                if _type == "VARCHAR":
                    expr.append(self.parse_varchar())
                elif _type == "@":
                    expr.append(self.parse_text())
                elif _type == "REPEAT":
                    expr.append(self.parse_repeat())
                elif _type == "ANY":
                    expr.append(self.parse_any())
                elif _type == "GROUP":
                    expr.append(self.parse_capture_group())
                else:
                    e = Error("", self.curr_token[1], self.curr_ident, self.curr_token[2], self.curr_token[3], self.source_code)
                    e.unexpected_identifier()
            elif self.curr_token[0] == Token.KEYWORD.name:
                _type = self.curr_token[1]
                self.curr_ident = _type
                expr.append(self.parse_keyword(_type))
            else:
                e = Error("", self.curr_token[1], self.curr_ident, self.curr_token[2], self.curr_token[3], self.source_code)
                e.unexpected_identifier()

        return expr
