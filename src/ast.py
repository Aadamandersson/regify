#!/usr/bin/env python3


class AstVarChar:
    def __init__(self, text, start, end=None):
        self.text = text
        self.start = start
        self.end = end
        self.escaped_chars = [
            '[', ']', '{', '}', '(', ')',
            '.', '|', '?', '*', '+', '\\', '/'
        ]

    def evaluate(self):
        escaped_text = ""
        for c in self.text:
            if c in self.escaped_chars:
                escaped_text += '\\'
            escaped_text += c
            
        if self.start is "*":
            return "[{0}]{{0,}}".format(escaped_text)
        elif self.start is '+':
            return "[{0}]{{1,}}".format(escaped_text)
        elif self.start is '?':
            return "[{0}]{{0,1}}".format(escaped_text)
        if self.end is None:
            return "[{0}]{{{1}}}".format(escaped_text, self.start)
        else:
            return "[{0}]{{{1},{2}}}".format(escaped_text, self.start, self.end)

    def __str__(self):
        return self.evaluate()



class AstText:
    def __init__(self, text, prev_tok, next_tok):
        self.text = text
        self.prev_tok = prev_tok
        self.next_tok = next_tok
        self.escaped_chars = [
            '[', ']', '{', '}', '(', ')',
            '.', '|', '?', '*', '+', '\\', '/'
        ]

    def evaluate(self):
        if self.next_tok == "VARCHAR" and self.text == "[":
            return "\\" + self.text
        elif self.prev_tok == "INLINE":
            return self.text

        # Else, escape the special characters
        ret = ""
        for c in self.text:
            if c in self.escaped_chars:
                ret += '\\'
            ret += c

        return ret

    def __str__(self):
        return self.evaluate()


class AstRepeat:
    def __init__(self, num, child):
        self.num = num
        self.child = child

    def evaluate(self):
        ret = "(?:"
        delim = ""
        for _ in range(0, int(self.num)):
            for j in range(0, len(self.child)):
                ret += delim + self.child[j].evaluate()
                if isinstance(self.child[j], AstAny):
                    delim = "|"
        return ret + ")"

    def __str__(self):
        return self.evaluate()


class AstAny:
    def __init__(self, children):
        self.children = children

    def evaluate(self):
        ret = "(?:"
        delim = "|"
        for i in range(0, len(self.children)):
            ret += self.children[i].evaluate()
            if i < len(self.children)-1:
                ret += delim
        return ret + ")"

    def __str__(self):
        return self.evaluate()


class AstNonCaptureGroup:
    def __init__(self, capture):
        self.capture = capture

    def evaluate(self):
        ret = "(?:"
        for i in range(0, len(self.capture)):
            ret += self.capture[i].evaluate()
        return ret + ")"

    def __str__(self):
        return self.evaluate()


class AstKeyword:
    def __init__(self, _type):
        self._type = _type

    def evaluate(self):
        if self._type == "INLINE":
            return ""
        elif self._type == "MORE":
            return ""
        elif self._type == "OR":
            return "|"
        elif self._type == "START":
            return "^"
        elif self._type == "END":
            return "$"
        return ""
