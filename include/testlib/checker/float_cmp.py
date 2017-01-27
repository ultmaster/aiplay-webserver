# Compare two sequences of real numbers, maximum absolute error is predefined in EPS
# Keep doing that until End Of File

from testlib import *

EPS = 1e-6


def float_cmp(out, ans, result):
    out_file = InputStream(out)
    ans_file = InputStream(ans)
    result_file = OutputStream(result)
    try:
        cnt = 0
        eof_expected = False
        ans_number = 0
        while True:
            try:
                ans_number = ans_file.read_real_number()
            except UnexpectedEOFError:
                eof_expected = True
            except JudgeException:
                raise UnexpectedAnswerError(ans_file.line)
            if eof_expected:
                out_file.read_eof()
                break
            else:
                out_number = out_file.read_real_number()
            if abs(out_number - ans_number) > EPS:
                raise InconsistentRealNumbersError(ans_number, out_number, out_file.line)
            cnt += 1
        result_file.report_ok('%d real number(s)' % cnt)
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    float_cmp('stdin', sys.argv[2], 'stdout')
