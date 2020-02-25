#!/usr/bin/env python3
import enum

class Token(enum.Enum):
    IDENT   = 0
    REP     = 1
    NUM     = 2
    L_PAREN = 3
    R_PAREN = 4
    EOF     = 5
    STRING  = 6
    COMMA   = 7


