#!/usr/bin/env python3

import sys
import os
# Run the tests with PyPi package if installed, otherwise locally
try:
    import regify
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.regify import generate_from_file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Expected argument: {} <filename>".format(sys.argv[0]))
        sys.exit(1)
    pattern = ""
    try:
        pattern = regify.generate_from_file(sys.argv[1])
    except NameError:
        pattern = generate_from_file(sys.argv[1])
    print("PATTERN:\n{}".format(pattern)) 






