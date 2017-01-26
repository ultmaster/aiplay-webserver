# Compare two real number lists, maximum absolute error is predefined in EPS
# Start with length of list, and then real numbers follow

from testlib import *

EPS = 1e-6


def float_ncmp(out, ans, result):
    out_file = InputStream(out)
    ans_file = InputStream(ans)
    result_file = OutputStream(result)
    try:
        try:
            ans_length = ans_file.read_integer()
        except JudgeException:
            raise UnexpectedAnswerError
        out_length = out_file.read_integer()
        if out_length != ans_length:
            raise InconsistentIntegersError(ans_length, out_length, out_file.line)
        for i in range(ans_length):
            try:
                ans_number = ans_file.read_real_number()
            except JudgeException:
                raise UnexpectedAnswerError
            out_number = out_file.read_real_number()
            if abs(out_number - ans_number) > EPS:
                raise InconsistentRealNumbersError(ans_number, out_number, out_file.line)
        try:
            ans_file.read_eof()
        except JudgeException:
            raise UnexpectedAnswerError
        out_file.read_eof()
        result_file.report_ok('%d real number(s)' % ans_length)
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    float_ncmp('stdin', sys.argv[2], 'stdout')
