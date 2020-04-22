import time
import sys

class LogTaskRun(object):
    """docstring for LogTaskRun."""

    def __init__(self, pattern, percentage, fails, task_run_id):
        self.pattern = pattern
        self.percentage = percentage
        self.fails = fails
        self.task_run_id = task_run_id
        self.time = time.time()


    def __str__(self):
        return 'task_run_id: {}\npercentage: {:.2f}%\nfails: {}\npattern: {}'.format(self.task_run_id, self.percentage, len(self.fails), self.pattern)
