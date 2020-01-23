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
    TEXT    = 7
    CHAR    = 8


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
            elif self.curr_char in [' ', '\t', '\n', '']:
                self.get_next_char()
            elif self.curr_char is ',':
                tokens.append((Token.COMMA.name, self.curr_char))
                self.get_next_char()
            else:
                tokens.append((self.curr_char, self.curr_char))
                self.get_next_char()


        return tokens


class NRange:
    def __init__(self, text, start, end=None):
        self.text = text
        self.start = start
        self.end = end

    def __str__(self):
        # [A-Z]{1,}
        if self.end is None:
            return "[{0}]{{{1}}}".format(self.text, self.start)
        else:
            return "[{0}]{{{1},{2}}}".format(self.text, self.start, self.end)


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
            print("Syntax error..\n")
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
                        #print(NRange(arg1, arg2))
                        expr.append(NRange(arg1, arg2))
                    else:
                        self.get_next_token()
                        arg3 = self.curr_token[1]
                        self.expect(Token.NUM.name)
                        expr.append(NRange(arg1, arg2, arg3))
                        #print(NRange(arg1, arg2, arg3))
            elif self.curr_token[0] is Token.IDENT.CHAR:
                pass    
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








