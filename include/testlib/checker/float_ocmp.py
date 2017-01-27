# Compare two real numbers, maximum absolute error is predefined in EPS
# One real number in file exactly, then it must be EOF

from testlib import *

EPS = 1e-6


def float_ocmp(out, ans, result):
    out_file = InputStream(out)
    ans_file = InputStream(ans)
    result_file = OutputStream(result)
    try:
        try:
            ans_number = ans_file.read_real_number()
            ans_file.read_eof()
        except JudgeException:
            raise UnexpectedAnswerError(ans_file.line)
        out_number = out_file.read_real_number()
        out_file.read_eof()
        if abs(out_number - ans_number) > EPS:
            raise InconsistentRealNumbersError(ans_number, out_number, out_file.line)
        result_file.report_ok('1 real number, error = %.12f' % abs(ans_number - out_number))
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    float_ocmp('stdin', sys.argv[2], 'stdout')
