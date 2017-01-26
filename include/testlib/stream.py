import re
import sys
from .exception import JudgeException

class InputStream:

    def __init__(self, file=None):
        self.buffer = ''
        self.buffered = False
        if file is None or file == 'stdin':
            self.file = sys.stdin
        else:
            try:
                self.file = open(file, "r")
            except OSError:
                self.file = None

    def update_buffer(self, func):
        def _update_buffer(*args, **kwargs):
            self.buffered = True
            empty = (self.buffer == '')
            if not empty:
                pattern = re.search(r'\s+', self.buffer)
                if pattern is not None and pattern.group() == self.buffer:
                    empty = True
            if empty:
                self.buffer = self.file.readline()
            return func(*args, **kwargs)
        return _update_buffer

    def read_all(self):
        if self.buffered:
            raise JudgeException('try to read the entire file from the middle')
        # Read All
        return self.file.read()

    def read_line(self):

        self.buffer = self.buffer[1:]
