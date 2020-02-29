#!/usr/bin/env python3
import os
import sys
import difflib
import reazy
import re

EXECUTABLE='./src/go.py'
TEST_FOLDER='./tests/generator'
DATASET_FOLDER='./datasets/'
NUM_OF_TESTS=10
VERBOSE=True

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


def run_test(num):
    print('========== TESTCASE {} =========='.format(num))
    # Create the paths to the dataset and hits which will be compared to
    dataset_path = '{}{}'.format(DATASET_FOLDER, '/q{}data.txt'.format(num))
    hits_path = '{}{}'.format(DATASET_FOLDER, '/q{}hits.txt'.format(num))

    # Read files and generate the regular expression
    current_dataset = read_file(dataset_path)
    current_target = read_file(hits_path)
    current_test = '{}{}'.format(TEST_FOLDER, '/q{}.rms'.format(num))
    pattern = reazy.generate_from_file(current_test)



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

for x in range(NUM_OF_TESTS):
    passed = run_test(x+1)
    if not passed:
        print ('Testcase {} failed!'.format(x+1))
        break
    print('\n')
