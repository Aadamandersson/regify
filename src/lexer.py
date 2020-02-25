#!/usr/bin/env python3
from token import Token



class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.curr_char = ''
        self.char_idx = -1
        self.col = 0
        self.row = 1

    def next_pos(self):
        self.char_idx += 1
        if self.curr_char is '\n':
            self.row += 1
            self.col = 0
        self.col += 1

    def get_next_char(self):
        self.next_pos()
        if self.char_idx < len(self.source_code):
            self.curr_char = self.source_code[self.char_idx] 
        else:
            self.curr_char = '\0'
    
    def read_next_char(self, next_char):
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
        str_val = ""
        self.get_next_char()

        prev_char = self.curr_char

        while self.curr_char is not '\0' and self.curr_char is not '"' or prev_char is '\\' and self.read_next_char('\\'):
            
            prev_char = self.curr_char 
            str_val += self.curr_char
            self.get_next_char()
 
        self.get_next_char()
        return str_val

    def skip_single_line_comment(self):
        while self.curr_char is not '\n':
            self.get_next_char()

    def lex(self):
        tokens = []
        while self.curr_char is not '\0':
            if self.curr_char.isalpha() or self.curr_char is '@':
                tokens.append((Token.IDENT.name, self.create_new_ident(), self.row, self.col))
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


