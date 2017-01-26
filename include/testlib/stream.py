import re
import sys

from .exception import *


def format_found_token(token):
    if "'" in token:
        return "'...'"
    if len(token) > 32:
        return "'%s...'" % token[:32]
    return "'%s'" % token


class InputStream:

    def __init__(self, file=None):
        self.buffer = ''
        self.line = 0
        if file is None or file == 'stdin':
            self.file = sys.stdin
        else:
            try:
                self.file = open(file, "r")
            except OSError:
                self.file = None

    def _get_all_from_buffer(self):
        try:
            self.buffer = ''
            _buffer = self.file.read()
            if not _buffer:
                raise EOFError
            return _buffer
        except EOFError:
            return ''

    def _get_a_line_from_buffer(self):
        if len(self.buffer) > 0:
            return self.buffer
        else:
            try:
                _buffer = self.file.readline()
                self.line += 1
                if not _buffer:
                    raise EOFError
                _buffer = _buffer.rstrip('\r\n')
                return _buffer
            except EOFError:
                raise UnexpectedEOFError('a line', self.line)

    def _get_a_token_from_buffer(self, usage='a token'):
        while True:
            _buffer = self.buffer.lstrip()
            if len(_buffer) > 0:
                _buffer = re.split(r'\s+', _buffer, 1)
                if len(_buffer) > 1:
                    self.buffer = _buffer[1]
                else:
                    self.buffer = ''
                return _buffer[0]
            self.buffer = self.file.readline()
            self.line += 1
            if not self.buffer:
                raise UnexpectedEOFError(usage, self.line)

    def read_rest_of_file(self):
        return self._get_all_from_buffer()

    def read_line(self):
        return self._get_a_line_from_buffer()

    def read_word(self):
        return self._get_a_token_from_buffer('word')

    def read_eof(self):
        try:
            self._get_a_token_from_buffer()
            raise UnexpectedTokenInFileError(self.line)
        except UnexpectedEOFError:
            pass

    def read_eol(self):
        try:
            _line = self._get_a_line_from_buffer()
            if _line.strip() != '':
                raise UnexpectedTokenInLineError(self.line)
        except UnexpectedEOFError:
            pass

    def read_integer(self):
        token = ''
        try:
            token = self._get_a_token_from_buffer('integer')
            return int(token)
        except (TypeError, ValueError):
            raise UnexpectedTypeError('an integer', format_found_token(token), self.line)

    def read_real_number(self):
        token = ''
        try:
            token = self._get_a_token_from_buffer('real number')
            return float(token)
        except (TypeError, ValueError):
            raise UnexpectedTypeError('a real number', format_found_token(token), self.line)


class OutputStream:

    def __init__(self, file=None):
        if file is None or file == 'stdout':
            self.file = sys.stdin
        else:
            try:
                self.file = open(file, "w")
            except OSError:
                raise JudgeException('cannot write output')

    def writeline(self, msg):
        self.file.write(str(msg) + '\n')

    def write(self, msg):
        self.file.write(str(msg))

    def report_ok(self, msg):
        self.writeline('ok, ' + msg)