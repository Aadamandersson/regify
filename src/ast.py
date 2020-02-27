#!/usr/bin/env python3


class AstVarChar:
    def __init__(self, text, start, end=None):
        self.text = text
        self.start = start
        self.end = end

    def evaluate(self):
        if self.start is '*':
            return "[{0}]{{0,}}".format(self.text)
        elif self.start is '+':
            return "[{0}]{{1,}}".format(self.text)
        elif self.start is '?':
            return "[{0}]{{0,1}}".format(self.text)
        if self.end is None:
            return "[{0}]{{{1}}}".format(self.text, self.start)
        else:
            return "[{0}]{{{1},{2}}}".format(self.text, self.start, self.end)
    
    def __str__(self):
        return self.evaluate()



class AstText:
    def __init__(self, text, next_tok):
        self.text = text
        self.next_tok = next_tok

    def evaluate(self):
        if self.next_tok in ["varchar", "VARCHAR"] and self.text == "[":
            return "\\" + self.text
        return self.text

    def __str__(self):
        return self.evaluate()


class AstRepeat:
    def __init__(self, num, child):
        self.num = num
        self.child = child

    def evaluate(self):
        ret = ""
        delim = ""    
        for _ in range(0, int(self.num)):
            for j in range(0, len(self.child)):
                ret += delim + self.child[j].evaluate()
                if isinstance(self.child[j], AstAny):
                    delim = "|"
        return ret

    def __str__(self):
        return self.evaluate()


class AstAny:
    def __init__(self, children):
        self.children = children
        
    def evaluate(self):
        ret = ""
        delim = ""
        for i in range(0, len(self.children)):
            ret += delim + self.children[i].evaluate()
            delim = "|"
        return ret

    def __str__(self):
        return self.evaluate()


class AstCaptureGroup:
    def __init__(self, capture):
        self.capture = capture

    def evaluate(self):
        ret = "("
        for i in range(0, len(self.capture)):
            ret += self.capture[i].evaluate()
        return ret + ")"

    def __str__(self):
        return self.evaluate()



