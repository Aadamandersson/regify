#!/usr/bin/env python3

# TODO: Create examples for all of the types
class Example:
    def __init__(self, ident):
        self.ident = ident
        self.varchar = """
'Example usage: VARCHAR("A-Z", 1, 2)
Note: Third argument is optional.'\n\n"""

    def __str__(self):
        if self.ident in ["varchar", "VARCHAR"]:
            return self.varchar
        return ""

class Error:
    def __init__(self, expected, found, ident, row, col, source_code):
        self.expected = expected
        self.found = found
        self.ident = ident
        self.row = row
        self.col = col
        self.source_code = source_code
        # red, green, end
        self.colors = ['\033[91m', '\033[92m', '\033[0m']
        self.example = Example(ident)
      
    def error_pos(self):
        content = self.source_code.splitlines()
        ret = ""
        for i in range(0, len(self.source_code.splitlines())-1):
            if i == self.row-2 and self.ident.lower() in content[i]:
                ret += "{}{}{}\n".format(self.colors[0], content[i], self.colors[2])
            elif i == self.row-1 and self.ident.lower() in content[i]:
                ret += "{}{}{}\n".format(self.colors[0], content[i], self.colors[2])
            else:
                ret += content[i] + "\n"
        
        return ret

    def __str__(self):
        se = "{}Syntax Error: {}".format(self.colors[0], self.colors[2])
        return """{}expected {} found {} in {} at line {}, col {}.\n{}{}\n
            """.format(se, self.expected, self.found, 
                    self.ident, self.row, self.col,
                    self.error_pos(), self.example)






