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

    def __init__(self, line=0):
        super().__init__()
        self.message = 'wrong answer'
        if line > 0:
            self.message += ' on line %d' % line


class UnexpectedTypeError(UnexpectedInputError):
    def __init__(self, expected, real, line):
        super().__init__(line)
        self.detail = '%s expected, but %s found' % (str(expected), str(real))


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
        self.detail = 'a real number %.12f expected, %.12f found, absolute error %.12f' % \
                      (expected, real, abs(expected - real))


class InconsistentIntegersError(InconsistentError):
    def __init__(self, expected, real, line):
        super().__init__(line)
        self.detail = 'an integer %d expected, %d found' % (expected, real)


class InconsistentTokensError(InconsistentError):
    def __init__(self, expected, real, line):
        super().__init__(line)
        self.detail = '%s expected, %s found' % (expected, real)


class UnexpectedAnswerError(JudgeException):

    def __init__(self, line):
        super().__init__()
        self.message = 'answer file is illegal on line %d' % line


class FileNotFoundError(JudgeException):

    def __init__(self, detail=''):
        super().__init__(detail)
        self.message = 'judge quits because file sent for judge is not found'
