#!/usr/bin/env python3
import re
import sys
import difflib

def read_file(fn):
    src = ""
    with open(fn, "r") as f:
        src = f.read()
    return src

def make_test(num, pattern):
    f_data = "datasets/q{}data.txt".format(num)
    f_hits = "datasets/q{}hits.txt".format(num)
    source = read_file(f_data)
    target = read_file(f_hits)
    result = re.findall(pattern, source)
    print(result)
    str_res = ""
    for i in result:
        str_res += i + '\n'
    d = difflib.Differ()
    diff = difflib.unified_diff([target], [str_res], lineterm='')
    print("TEST: {}".format(num))
    return ('\n'.join(diff) is '', '\n'.join(diff))

if __name__ == '__main__':
    passed = True
    #passed, out = make_test(1, '\[[0-9]{4}::]')
    if passed is True:
        print("Passed")
    else:
        print("Failed: \n{}\n".format(out))

    #passed, out = make_test(6, '[-|>|<]{12}')
    
    if passed is True:
        print("Passed")
    else:
        print("Failed: \n{}\n".format(out))
    #grep -o '\([\.,][:;]\{2,3\}\)\{2\}\|\[[/\\][A-Z][a-z]\{,\}]'
#([\.,][:;]{2,3}){2}|\[[/\\][A-Z][a-z]{0,}]
    passed, out = make_test(10, '([\.,][:;]{2,3}){2}|\[[/\\][A-Z][a-z]{0,}]')
    
    if passed is True:
        print("Passed")
    else:
        print("Failed: \n{}\n".format(out))

