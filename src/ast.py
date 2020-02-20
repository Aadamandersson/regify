#!/usr/bin/env python3


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
        for _ in range(0, self.num):
            ret += self.child
        return ret
        
    def __new__(self, num, child):
        ret = ""
        for _ in range(0, int(num)):
            ret += child
        return ret

class NAny:
    def __init__(self, children):
        self.children = children
        
    def __str__(self):
        ret = ""
        delim = ""
        for i in range(0, len(self.children)):
            ret += delim + self.children[i]
            delim = "|"
        return ret

    def __new__(self, children):
        ret = ""
        delim = ""
        for i in range(0, len(children)):
            ret += delim + children[i]
            delim = "|"
        return ret
