#!/usr/bin/env python3
import enum

class Token(enum.Enum):
    IDENT   = 0
    NUM     = 1
    L_PAREN = 2
    R_PAREN = 3
    EOF     = 4
    STRING  = 5
    COMMA   = 6
