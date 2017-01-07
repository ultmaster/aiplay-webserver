import os
from .compiler import try_to_compile


# Tester: to test whether a submission is a valid submission
class Tester(object):

    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    def test(self):
        if not try_to_compile(self.submission):
            return False


