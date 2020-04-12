#!/usr/bin/env python3
from .token import Token

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.curr_char = ''
        self.char_idx = -1
        self.col = 0
        self.row = 1
        self.keywords = [
            "INLINE",
            "OR",
            "MORE",
            "START",
            "END",
            "UNTIL"
        ]

    def next_pos(self):
        """
            Calculates the position for column and row number
            in the source which is  passed to the parser
            for better error handling.
        """
        self.char_idx += 1
        if self.curr_char is '\n':
            self.row += 1
            self.col = 0
        self.col += 1

    def get_next_char(self):
        """
            Gets the next character from the source code.
        """
        self.next_pos()
        if self.char_idx < len(self.source_code):
            self.curr_char = self.source_code[self.char_idx]
        else:
            self.curr_char = '\0'

    def read_next_char(self, next_char):
        """
            Peeks one character in source code
            to check if it's a certain char
        """
        self.get_next_char()
        if self.curr_char is not next_char:
            return False
        self.curr_char = ' '
        return True

    def create_new_num(self):
        num = ""
        while self.curr_char.isdigit():
            num += self.curr_char
            self.get_next_char()
        return num

    def create_new_ident(self):
        ident = ""
        while self.curr_char.isalpha() and self.curr_char is not '@':
            ident += self.curr_char
            self.get_next_char()
        if self.curr_char is '@':
            ident = self.curr_char
            self.get_next_char()

        return ident

    def create_new_str(self):
        str_val = ''
        self.get_next_char()
        prev_char = ""
        escaped = False
        while self.curr_char is not '\0':
            if prev_char is '\\' and self.curr_char is '"':
                escaped = True
            if prev_char is '"' and self.curr_char is '"':
                self.get_next_char()
                return str_val
            elif self.curr_char is '"' and not escaped:
                self.get_next_char()
                return str_val

            if prev_char is '"':
                str_val = str_val[:-1]
            str_val += self.curr_char
            prev_char = self.curr_char
            self.get_next_char()

        self.get_next_char()
        return str_val

    def skip_single_line_comment(self):
        while self.curr_char is not '\n' and self.curr_char is not '\0':
            self.get_next_char()

    def lex(self):
        """
            Tokenizes the source code.
            Returns all the tokens created.
        """
        tokens = []
        while self.curr_char is not '\0':
            if self.curr_char.isalpha() or self.curr_char is '@':
                _id = self.create_new_ident()
                if _id in self.keywords:
                    tokens.append((Token.KEYWORD.name, _id, self.row, self.col))
                else:
                    tokens.append((Token.IDENT.name, _id, self.row, self.col))
            elif self.curr_char.isdigit():
                tokens.append((Token.NUM.name, self.create_new_num(), self.row, self.col))
            elif self.curr_char in ['*', '+', '?']:
                tokens.append((Token.REP.name, self.curr_char, self.row, self.col))
                self.get_next_char()
            elif self.curr_char is '(':
                tokens.append((Token.L_PAREN.name, self.curr_char, self.row, self.col))
                self.get_next_char()
            elif self.curr_char is ')':
                tokens.append((Token.R_PAREN.name, self.curr_char, self.row, self.col))
                self.get_next_char()
            elif self.curr_char is '"':
                tokens.append((Token.STRING.name, self.create_new_str(), self.row, self.col))
            elif self.curr_char in [' ', '\t', '\n', '']:
                self.get_next_char()
            elif self.curr_char is ',':
                tokens.append((Token.COMMA.name, self.curr_char, self.row, self.col))
                self.get_next_char()
            elif self.curr_char is '#':
                self.skip_single_line_comment()
            else:
                tokens.append((self.curr_char, self.curr_char, self.row, self.col))
                self.get_next_char()

        tokens.append((Token.EOF.name, ""))

        return tokens


