# Compare file is not included in __init__.py
# Please include testlib.compare to use it

from .stream import *
from .exception import *


class Compare:

    EXPECT_INTEGER = 0
    EXPECT_REAL_NUMBER = 1
    EXPECT_WORD = 2
    EXPECT_LINE = 3

    def __init__(self, out, ans):
        self.out_file = InputStream(out)
        self.ans_file = InputStream(ans)
        self.out_eof, self.ans_eof = False, False

        self.eps = 1e-6
        self.expect = Compare.EXPECT_WORD
        self.filter_blank_line_at_eof = False
        self.read_function = InputStream.read_word
        self.compare_content = lambda x, y: x == y
        self.inconsistent_error = InconsistentTokensError
        self.description = 'word'

    def _read(self, func):
        while True:
            try:
                self.ans_content = func(self.ans_file)
            except UnexpectedEOFError:
                self.ans_eof = True
            except JudgeException:
                raise UnexpectedAnswerError(self.ans_line())

            try:
                self.out_content = func(self.out_file)
            except UnexpectedEOFError:
                self.out_eof = True

            if self.ans_eof and self.out_eof:  # ans and out both come to an end
                return False
            if not (self.ans_eof or self.out_eof):  # ans and out both are in a middle
                return True
            if not self.filter_blank_line_at_eof:  # for no-privilege cases
                return True
            if self.ans_eof and not self.is_believed_eof(self.out_content):  # actually something is wrong
                return True
            if self.out_eof and not self.is_believed_eof(self.ans_content):  # bad luck!
                return True
            # else read again

    def out_line(self):
        return self.out_file.line

    def ans_line(self):
        return self.ans_file.line

    def set_eps(self, eps):
        self.eps = eps

    def set_expectation(self, expect):
        self.expect = expect
        self.filter_blank_line_at_eof = False
        if expect == Compare.EXPECT_INTEGER:
            self.read_function = InputStream.read_integer
            self.compare_content = lambda x, y: x == y
            self.inconsistent_error = InconsistentIntegersError
            self.description = 'integer'
        elif expect == Compare.EXPECT_REAL_NUMBER:
            self.read_function = InputStream.read_real_number
            self.compare_content = lambda x, y: abs(x - y) < self.eps
            self.inconsistent_error = InconsistentRealNumbersError
            self.description = 'real number'
        elif expect == Compare.EXPECT_WORD:
            self.read_function = InputStream.read_word
            self.compare_content = lambda x, y: x == y
            self.inconsistent_error = InconsistentTokensError
            self.description = 'word'
        elif expect == Compare.EXPECT_LINE:
            self.filter_blank_line_at_eof = True
            self.read_function = InputStream.read_line
            self.compare_content = lambda x, y: x.rstrip() == y.rstrip()
            self.inconsistent_error = InconsistentTokensError
            self.description = 'line'

    def is_believed_eof(self, content):
        if content is None:
            return True
        if not isinstance(content, str):
            return False
        if self.filter_blank_line_at_eof and content.strip() == '':
            return True
        return False

    # If ans and out both reaches eof, return False
    # otherwise return True (unless throwing exception)
    def compare_next(self, expect):
        self.set_expectation(expect)
        if not self._read(self.read_function):
            return False
        if self.ans_eof:
            raise UnexpectedTokenInFileError(self.out_line())
        if self.out_eof:
            raise UnexpectedEOFError(format_found_token(self.ans_content), self.out_line())
        if not self.compare_content(self.out_content, self.ans_content):
            raise self.inconsistent_error(format_found_token(self.ans_content),
                                          format_found_token(self.out_content),
                                          self.out_line())
        return True

    def assert_eof(self):
        try:
            self.ans_file.read_eof()
        except JudgeException:
            raise UnexpectedAnswerError(self.ans_line())
        self.out_file.read_eof()

    def assert_eol(self):
        try:
            self.ans_file.read_eol()
        except JudgeException:
            raise UnexpectedAnswerError(self.ans_line())
        self.out_file.read_eol()


def _compare_until_eof(out, ans, result, expect, eps=None):
    result_file = OutputStream(result)
    try:
        cmp = Compare(out, ans)
        if eps is not None:
            cmp.set_eps(eps)
        cnt = 0
        while cmp.compare_next(expect):
            cnt += 1
        result_file.report_ok('%d %s(s)' % (cnt, cmp.description))
    except JudgeException as e:
        result_file.writeline(e)


def _compare_for_cnt(out, ans, result, expect, eps=None):
    result_file = OutputStream(result)
    try:
        cmp = Compare(out, ans)
        if eps is not None:
            cmp.set_eps(eps)
        if not cmp.compare_next(Compare.EXPECT_INTEGER):
            raise UnexpectedAnswerError(cmp.ans_line())
        ans_length = cmp.ans_content
        for i in range(ans_length):
            if not cmp.compare_next(expect):
                raise UnexpectedAnswerError(cmp.ans_line())
        cmp.assert_eof()
        result_file.report_ok('%d %s(s)' % (ans_length, cmp.description))
    except JudgeException as e:
        result_file.writeline(e)


# File compare filtering out blank lines at eof and spaces at eol

def file_cmp(out, ans, result):
    _compare_until_eof(out, ans, result, Compare.EXPECT_LINE)


# Real Number Compare

def float_cmp(out, ans, result, eps=None):
    _compare_until_eof(out, ans, result, Compare.EXPECT_REAL_NUMBER, eps)


def float_ncmp(out, ans, result, eps=None):
    _compare_for_cnt(out, ans, result, Compare.EXPECT_REAL_NUMBER, eps)


def float_ocmp(out, ans, result, eps=None):
    result_file = OutputStream(result)
    try:
        cmp = Compare(out, ans)
        if eps is not None:
            cmp.set_eps(eps)
        if not cmp.compare_next(Compare.EXPECT_REAL_NUMBER):
            raise UnexpectedAnswerError(cmp.ans_line())
        cmp.assert_eof()
        result_file.report_ok('1 real number, output %.12f, answer %.12f, error %.12f' %
                              (cmp.out_content, cmp.ans_content, abs(cmp.ans_content - cmp.out_content)))
    except JudgeException as e:
        result_file.writeline(e)


# Integer Compare

def int_cmp(out, ans, result):
    _compare_until_eof(out, ans, result, Compare.EXPECT_INTEGER)


def int_ocmp(out, ans, result):
    result_file = OutputStream(result)
    try:
        cmp = Compare(out, ans)
        if not cmp.compare_next(Compare.EXPECT_INTEGER):
            raise UnexpectedAnswerError(cmp.ans_line())
        cmp.assert_eof()
        result_file.report_ok('1 integer: %d' % cmp.ans_content)
    except JudgeException as e:
        result_file.writeline(e)


def int_ncmp(out, ans, result):
    _compare_for_cnt(out, ans, result, Compare.EXPECT_INTEGER)


# Word Compare

def word_cmp(out, ans, result):
    _compare_until_eof(out, ans, result, Compare.EXPECT_WORD)


def word_ocmp(out, ans, result):
    result_file = OutputStream(result)
    try:
        cmp = Compare(out, ans)
        if not cmp.compare_next(Compare.EXPECT_WORD):
            raise UnexpectedAnswerError(cmp.ans_line())
        cmp.assert_eof()
        result_file.report_ok('1 word: %s' % format_found_token(cmp.ans_content))
    except JudgeException as e:
        result_file.writeline(e)


def word_ncmp(out, ans, result):
    _compare_for_cnt(out, ans, result, Compare.EXPECT_WORD)
