class JudgeException(Exception):

    def __init__(self, detail=''):
        self.message = 'judge failed for mysterious error'
        self.detail = detail

    def __str__(self):
        if self.detail == '':
            return self.message
        else:
            return '%s: %s' % (self.message, self.detail)


class UnexpectedInputError(JudgeException):

    def __init__(self, line=0):
        super().__init__()
        self.message = 'idleness limit exceeded, unexpected input'
        if line > 0:
            self.message += ' on line %d' % line


class InconsistentError(JudgeException):

    def __init__(self, msg, line=0):
        super().__init__()
        self.message = 'wrong answer'
        if line > 0:
            self.message += ' on line %d' % line
        self.detail = msg


class UnexpectedTypeError(UnexpectedInputError):
    def __init__(self, expected, real, line):
        super().__init__(line)
        self.detail = 'expected %s, but %s found' % (expected, real)


class UnexpectedEOFError(UnexpectedTypeError):
    def __init__(self, expected='a token', line=0):
        super().__init__(expected, 'eof', line)


class UnexpectedTokenInFileError(UnexpectedTypeError):
    def __init__(self, line):
        super().__init__('eof', 'another token', line)


class UnexpectedTokenInLineError(UnexpectedTypeError):
    def __init__(self, line):
        super().__init__('end of line', 'another token', line)


class InconsistentRealNumbersError(InconsistentError):
    def __init__(self, expected, real, line):
        super().__init__(line)
        self.detail = 'expected %.12f, %.12f found, absolute error %.12f' % (expected, real, abs(expected - real))


class InconsistentIntegersError(InconsistentError):
    def __init__(self, expected, real, line):
        super().__init__(line)
        self.detail = 'expected %d, %d found' % (expected, real)