#!/usr/bin/env python3
import regify
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Expected argument: {} <filename>".format(sys.argv[0]))
        sys.exit(1)

    pattern = regify.generate_from_file(sys.argv[1])
    print("PATTERN:\n{}".format(pattern))






