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

    def __init__(self):
        super().__init__()
        self.message = 'idleness limit exceeded, unexpected input'


class InconsistentError(JudgeException):

    def __init__(self):
        super().__init__()
        self.message = 'wrong answer'


class UnexpectedTypeError(UnexpectedInputError):

    def __init__(self, expected, real):
        super().__init__()
        self.detail = 'expected a(n) %s, but %s found' % (expected, real)

