from .program import Program
from config import *
from .utils import *

# Tester: to test whether a submission is a valid submission
class Tester(object):

    def __init__(self, program):
        self.program = program
        self.message = ''

    def test(self):
        if not self.test_compile():
            return { 'error': ERROR_CODE[COMPILE_ERROR], 'message': self.message }
        if not self.test_run():
            return { 'error': ERROR_CODE[PRETEST_FAILED], 'message': self.message }
        return { 'error' : ERROR_CODE[PRETEST_PASSED] }

    def test_compile(self):
        if not self.program.compile():
            self.error = 1
            self.message = read_partial_data_from_file(self.program.compile_out_path, 1024)
            if self.message == '':
                self.message = read_partial_data_from_file(self.program.compile_log_path, 1024)
            return False
        return True

    def test_run(self):
        # TODO
        return True