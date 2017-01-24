from .program import Program
from config import *
from .utils import *

# Tester: to test whether a submission is a valid submission
class Tester(object):

    def __init__(self, program, judge=None):
        self.program = program
        self.judge = judge
        self.error = PRETEST_PASSED
        self.message = ''

    def test(self):
        if self.test_compile() and self.judge is not None:
            self.test_run()
        self.message = 'Submission #%d:' % self.program.submission_id
        return { 'code' : self.error, 'message' : self.message }

    def test_compile(self):
        if not self.program.compile():
            self.error = COMPILE_ERROR
            self.message = read_partial_data_from_file(self.program.compile_out_path, 1024)
            if self.message == '':
                self.message = read_partial_data_from_file(self.program.compile_log_path, 1024)
            self.message = 'sub #%d:\n' + self.message
            return False
        return True

    def test_run(self):
        # TODO
        return True