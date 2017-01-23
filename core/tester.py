from .program import Program
from config import COMPILE_ERROR

# Tester: to test whether a submission is a valid submission
class Tester(object):

    def __init__(self, program):
        self.program = program
        self.error = ''
        self.message = ''

    def test(self):
        if not self.test_compile() or not self.test_run():
            return { 'error': COMPILE_ERROR, 'message': self.message }
        return { 'error': 0 }

    def test_compile(self):
        if not self.program.compile():
            self.error = 1
            with open(self.program.compile_out_path, "r") as f:
                self.message = f.read(1024)
            if self.message == '':
                with open(self.program.compile_log_path, "r") as f:
                    self.message = f.read(1024)
            if self.message >= 1023:
                self.message += '\n......'
            return False
        return True

    def test_run(self):
        # TODO
        return True