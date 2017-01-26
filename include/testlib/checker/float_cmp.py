# Compare two real numbers, maximum absolute error is predefined in EPS

from testlib import *
import sys

EPS = 1e-6

if __name__ == '__main__':
    in_file, out_file, ans_file, new_file, result_file = \
        registerJudge(sys.argv[1], 'stdin', sys.argv[2], sys.argv[3], 'stdout')
    try:
        cnt = 0
        eof_expected = False
        ans_number = 0
        while True:
            try:
                ans_number = ans_file.read_real_number()
            except UnexpectedEOFError:
                eof_expected = False
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