import os


# Tester: to test whether a submission is a valid submission
class Tester(object):

    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    def test(self):
        pass

