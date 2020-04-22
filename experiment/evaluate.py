import os
import sys
import argparse
import pickle
import re
import tabulate
from logtaskrun import LogTaskRun

argparser = argparse.ArgumentParser(description='Experiment manager for REgify')

argparser.add_argument('--dir', dest='directory', help='path to directory containing log information', required=True)
argparser.add_argument('--dest', dest='dest', help='path to file where the evaluation data will be written to', required=True)

args = argparser.parse_args()

LOGDIR = args.directory
OUTFILE = args.dest



for file in sorted(os.listdir(LOGDIR)):
    divided = file.split('_')
    lang = divided[2].split('.')[0]
    task_number = divided[1]

    print('========== [TASK {} in {}] =========='.format(task_number, lang))
    with open('{}/{}'.format(LOGDIR, file), 'rb') as logfile:
        task_run = pickle.load(logfile)

        last_time = 0
        last_pattern = 0
        run_counter = 0
        for run in task_run:
            print('Run {}\n\tPercentage: {:.2f}%'.format(run.task_run_id, run.percentage))
            print('\tAmount of characters modified: {}'.format(len(run.pattern) - last_pattern))

            if last_time != 0:
                print('\tTime spent: {:.2f}s'.format(run.time - last_time))
            last_time = run.time
            last_pattern = len(run.pattern)

            run_counter += 1
            if run.percentage == 100.0:
                break

        print('TOTAL RUNS: {}'.format(run_counter))


