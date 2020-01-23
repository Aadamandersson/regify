#!/usr/bin/env python3
import sys
import enum

class Token(enum.Enum):
    IDENT   = 0
    NUM     = 1
    L_PAREN = 2
    R_PAREN = 3
    EOF     = 4
    STRING  = 5
    COMMA   = 6



class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.curr_char = ''
        self.char_idx = -1

    def get_next_char(self):
        self.char_idx += 1
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
        
    def lex(self):
        tokens = []
        while self.curr_char is not '\0':
            if self.curr_char.isalpha():
                ident = ""
                while self.curr_char.isalpha():
                    ident += self.curr_char
                    self.get_next_char()
                tokens.append((Token.IDENT.name, ident))
            elif self.curr_char.isdigit():
                num = ""
                while self.curr_char.isdigit():
                    num += self.curr_char
                    self.get_next_char()
                tokens.append((Token.NUM.name, num))
            elif self.curr_char is '(':
                tokens.append((Token.L_PAREN.name, self.curr_char))
                self.get_next_char()
            elif self.curr_char is ')':
                tokens.append((Token.R_PAREN.name, self.curr_char))
                self.get_next_char()
            elif self.curr_char is '"':
                str_val = ""
                self.get_next_char()
                while self.curr_char is not '\0' and self.curr_char is not '"':
                    str_val += self.curr_char
                    self.get_next_char()
                self.get_next_char()
                tokens.append((Token.STRING.name, str_val))
            elif self.curr_char in [self.curr_char.isspace(), '\t', '\n']:
                self.get_next_char()
            elif self.curr_char is ',':
                tokens.append((Token.COMMA.name, self.curr_char))
                self.get_next_char()
            else:
                self.get_next_char()


        return tokens










#grep -o '\[[A-Z][a-z]\{,\}->]'
#[range(“A-Z”,1)range(“a-z”, *)->]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Expected argument: {} <filename>".format(sys.argv[0]))
        sys.exit(1)

    source_code = ""
    with open(sys.argv[1], "r") as f:
        source_code = f.read()
    lexer = Lexer(source_code)
    tokens = lexer.lex()
    
    for t in tokens:
        print(t)









