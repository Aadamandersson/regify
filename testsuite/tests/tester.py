#!/usr/bin/env python3
import os
import sys
import difflib
import re
from regify import regify


EXECUTABLE='./testsuite/tests/go.py'
TEST_FOLDER='./testsuite/tests/generator/'
DATASET_FOLDER='./testsuite/datasets/'
TEST_CASES = "./testsuite/tests/testcases.txt"
START_TEST_NR=0
NUM_OF_TESTS=10
NEXT_LEVEL=False
VERBOSE=True
if NEXT_LEVEL:
    START_TEST_NR=10
    NUM_OF_TESTS+=1
    TEST_FOLDER+="next_level"
    DATASET_FOLDER+="next_level"


def read_file(fn):
    src = ""
    with open(fn, "r") as f:
        src = f.read()
    return src

def head_of_file(path, lines):
    data = ""
    with open(path) as myfile:
        firstNlines=myfile.readlines()[0:lines]
        maxlen = lines

        if (lines > len(firstNlines)):
            maxlen = len(firstNlines)

        for x in range(maxlen):
            data += firstNlines[x]

    return data


def run_test(testcase):
    print('========== TESTCASE {} =========='.format(testcase[0]))
    # Create the paths to the dataset and hits which will be compared to
    dataset_path = testcase[1]
    hits_path = testcase[2]
    current_test = testcase[3]

    # Read files and generate the regular expression
    current_dataset = read_file(dataset_path)
    current_target = read_file(hits_path)
    pattern = regify.generate_from_file(current_test)


    if VERBOSE:
        #print("[INFO] Dataset: {}".format(current_dataset))
        #print("[INFO] Target data path: {}".format(current_dataset))

        print("[INFO] HEAD of {}:  \n{}".format(dataset_path, head_of_file(dataset_path, 5)))
        print("[INFO] HEAD of {}:  \n{}".format(hits_path, head_of_file(hits_path, 5)))

        print("[INFO] Test path: {}".format(current_test))
        print("[INFO] Source code:\n{}".format(read_file(current_test)))

        print("[INFO] Generated pattern:\n{}".format(pattern))


    # Pass the pattern generated to RE and find all matches in the loaded dataset
    m = re.findall(pattern, current_dataset)

    # convert the list to a string, required for comparing with "difflib"
    res = ""
    for r in m:
        res += r + '\n'

    # Diff the target ouput with the output we got from our generated regex
    # Two differnt objects are required for printing... bug?
    diff = difflib.unified_diff([current_target], [res])
    diff2 = difflib.unified_diff([current_target], [res])

    success = True
    if '\n'.join(diff) is not '':
        print("MATCH FAILED:\n{}".format('\n'.join(diff2)))
        success = False
    else:
        print("SUCCESSFULLY MATCHED")

    print('=================================')
    return success

def get_testcases(path):
    csv = []
    with open(path, "r") as testcases:
        lines = testcases.readlines()
        lines = [line.rstrip('\n') for line in lines]
        for line in lines:
            csv.append(line.split(' '))

    return csv

# for x in range(START_TEST_NR, NUM_OF_TESTS):
#     passed = run_test(x+1)
#     if not passed:
#         print ('Testcase {} failed!'.format(x+1))
#         break
#     print('\n')


tests = get_testcases(TEST_CASES)
print('[+] Loaded {} testcases'.format(len(tests)))
for x in range(START_TEST_NR, len(tests)):
    passed = run_test(tests[x])
    if not passed:
        print ('Testcase {} failed!'.format(tests[x][0]))
        break
