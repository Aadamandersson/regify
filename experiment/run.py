import os
import sys
import difflib
from difflib import SequenceMatcher
import re
#import regify
import argparse
#from simplecrypt import encrypt, decrypt
import itertools
import pickle
import time

sys.path.insert(1, '/Users/ludwighansson/Desktop/rms/src')
from regify import regify

argparser = argparse.ArgumentParser(description='Experiment manager for REgify')

argparser.add_argument('task',  help='select which task should be run by entering its number')

arguments = argparser.parse_args()
TESTCASE_NUM=arguments.task

REGEX='task_{}/regex.re'.format(TESTCASE_NUM)
DATASET_PATH='task_{}/data/dataset.txt'.format(TESTCASE_NUM)
VAL_DATA_PATH='task_{}/data/valid.txt'.format(TESTCASE_NUM)

LOG_PATH='log/task_{}.txt'.format(TESTCASE_NUM)

class LogTaskRun(object):
    """docstring for LogTaskRun."""

    def __init__(self, pattern, percentage, fails, task_run_id):
        self.pattern = pattern
        self.percentage = percentage
        self.fails = fails
        self.task_run_id = task_run_id

    def __str__(self):
        return 'task_run_id: {}\npercentage: {:.2f}%\nfails: {}\npattern: {}'.format(self.task_run_id, self.percentage, self.fails, self.pattern)

# CAPTURE
# 1. Runs
# 2. Time between
# 3. Changes

def read_file(fn):
    src = ""
    with open(fn, "r") as f:
        src = f.read()
    return src

def read_crypted_file(fn):
    src = ""
    with open(fn, "rb") as f:
        src = f.read()
    return decrypt('VEFTSzE=', src).decode("utf-8")

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

def get_match_percentage(usr_input, valid):
    percentage = 0.0
    percentage_list = []
    idx = 0
    for match, val in itertools.zip_longest(usr_input, valid):
        if (match is None):
            match = ''
        if (val is None):
            val = ''
        word_percent = SequenceMatcher(None, match, val).ratio()
        if word_percent != 1.0:
            percentage_list.append({ 'index':idx, 'target':val, 'actual':match, 'percent':word_percent})
        idx += 1
        percentage += word_percent

    return (percentage / idx * 100, percentage_list)

def store_logdata(pattern, percentage, fails):

    if not os.path.exists('log'):
        os.makedirs('log')

    logdata = []

    if os.path.exists(LOG_PATH):
        logdata = pickle.load(open(LOG_PATH, 'rb'))

    logdata.append(LogTaskRun(pattern, percentage, fails, len(logdata)))
    pickle.dump(logdata, open(LOG_PATH, 'wb+'))
    print(logdata[-1])

def run_task():
    print('========== EXPERIMENT TASK {} =========='.format(TESTCASE_NUM))

    # Read files and generate the regular expression
    dataset = read_file(DATASET_PATH).split('\n')
    current_target = read_file(VAL_DATA_PATH)
    pattern = regify.generate_from_file(REGEX)


    # Pass the pattern generated to RE and find all matches in the loaded dataset
    matches = []
    for line in dataset:
        for match in re.findall(pattern, line):
            matches.append(match)
            with open('output.txt', 'a+') as file:
                file.write(match + '\n')

    val = []
    with open(VAL_DATA_PATH, 'r') as file:
        for line in file.readlines():
            val.append((line.split('\n')[0]))
            #print(val[-1])


    percentage, failed_matches = get_match_percentage(matches, val)

    if (len(failed_matches) > 0):
        for idx in failed_matches:
            print('{}: {:.2f}%   {}   ->   {}'.format(idx['index'], idx['percent'] * 100, idx['target'], idx['actual']))
    else:
        print('Everything matched sucessfully')
    print('================ STATS ================'.format(TESTCASE_NUM))
    print('Total match percentage: {:.2f}%'.format(percentage))
    print('Amount of 100% matches: {} of {} '.format(len(val) - len(failed_matches), len(val)))

    store_logdata(pattern, percentage, failed_matches);

    return percentage

run_task()
