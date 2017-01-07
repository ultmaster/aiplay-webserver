import os
from .compiler import try_to_compile

class Handler(object):
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    def run(self):
        if not self.compile():
            raise BaseException("Some accident just happened.")

    def compile(self):
        for submission in self.submissions:
            if not try_to_compile(submission):
                return False
        if not try_to_compile(self.judge):
            return False
        return True
