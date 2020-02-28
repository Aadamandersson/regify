import os
import sys
import difflib
import reazy
import re

EXECUTABLE='src/go.py'
TEST_FOLDER='../tests/generator'
DATASET_FOLDER='../datasets/'
NUM_OF_TESTS=9
VERBOSE=True

def read_file(fn):
    src = ""
    with open(fn, "r") as f:
        src = f.read()
    return src

def run_test(num):
    print('========== TESTCASE {} =========='.format(num))
    current_dataset = read_file('{}{}'.format(DATASET_FOLDER, '/q{}data.txt'.format(num)))
    current_target = read_file('{}{}'.format(DATASET_FOLDER, '/q{}hits.txt'.format(num)))
    current_test = '{}{}'.format(TEST_FOLDER, '/q{}.rms'.format(num))
    pattern = reazy.generate_from_file(current_test)

    success = True

    if VERBOSE:
        #print("[INFO] Dataset: {}".format(current_dataset))
        #print("[INFO] Target data path: {}".format(current_dataset))
        print("[INFO] Test path: {}".format(current_test))
        print("[INFO] Generated pattern:\n{}".format(pattern))

    m = re.findall(pattern, current_dataset)
    res = ""
    for r in m:
        res += r + '\n'

    diff = difflib.unified_diff([current_target], [res])
    diff2 = difflib.unified_diff([current_target], [res])
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
