import os
from .compiler import try_to_compile
from .program import Submission


class Handler(object):
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        self.submission_list = []
        for submission in self.submissions:
            self.submission_list.append(Submission(submission, self.round_config))

    def run(self):
        if not self.compile():
            raise BaseException("Some accident just happened.")

    def compile(self):
        for submission in self.submission_list:
            if not submission.compile():
                return False
        if not Submission(self.judge, self.round_config).compile():
            return False
        return True
