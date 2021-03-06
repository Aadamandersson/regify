#!/usr/bin/env python3
import sys
import difflib

# TODO: Create examples for all of the types
class Example:
    def __init__(self, ident):
        self.ident = ident
        self.varchar = """
'Example usage: VARCHAR("A-Z", 1, 2)
Note: Third argument is optional.'\n\n"""

    def __str__(self):
        if self.ident == "VARCHAR":
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
        self.identifiers = [
            "VARCHAR", "REPEAT",
            "ANY", "GROUP"
        ]
          
    def highlight_error(self):
        content = self.source_code.splitlines()
        ret = ""
        for i in range(0, len(self.source_code.splitlines())):
            if i+1 == self.row and self.ident in content[i]:
                ret += "{}{}{}\n".format(self.colors[0], content[i], self.colors[2])
            elif i+2 == self.row and self.ident in content[i] and self.found in [',', ')']:
                ret += "{}{}{}\n".format(self.colors[0], content[i], self.colors[2])
            else:
                ret += content[i] + "\n"

        return ret
    
    def invalid_nr_of_args(self):
        se = "{}ValueError: {}".format(self.colors[0], self.colors[2])
        ret = """{}Invalid number of arguments. Expected {} or {} in {} at line {}, col {}.\n{}{}\n
            """.format(se, self.expected, self.found, 
                    self.ident, self.row, self.col,
                    self.highlight_error(), self.example)
        print(ret)
        sys.exit(1)
       
    def unexpected_argument(self):
        # example?
        se = "{}TypeError: {}".format(self.colors[0], self.colors[2])
        ret = """{}{} got an unexpected keyword argument '{}' at line {}, col {}.\n{}\n
            """.format(se, self.found, self.ident, self.row, self.col,
                    self.highlight_error())
        print(ret)
        sys.exit(1)
    
    def unexpected_identifier(self):
        se = "{}SyntaxError: {}".format(self.colors[0], self.colors[2])
        prop = difflib.get_close_matches(self.found.upper(), self.identifiers)
        full_prop = ""
        if prop:
            full_prop = "Did you mean {}?\n".format(prop[0])

        ret = """{}unexpected identifier {} at line {}, col {}.\n{}\n{}{}\n
            """.format(se, self.found, 
                    self.row, self.col, full_prop,
                    self.highlight_error(), self.example)
        print(ret)
        sys.exit(1)

    def __str__(self):
        se = "{}SyntaxError: {}".format(self.colors[0], self.colors[2])
        return """{}expected {} found {} in {} at line {}, col {}.\n{}{}\n
            """.format(se, self.expected, self.found, 
                    self.ident, self.row, self.col,
                    self.highlight_error(), self.example)






