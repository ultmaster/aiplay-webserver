# Compare two integers
# One integer in file exactly, then it must be EOF

from testlib import *


def int_ocmp(out, ans, result):
    out_file = InputStream(out)
    ans_file = InputStream(ans)
    result_file = OutputStream(result)
    try:
        try:
            ans_number = ans_file.read_integer()
            ans_file.read_eof()
        except JudgeException:
            raise UnexpectedAnswerError
        out_number = out_file.read_integer()
        out_file.read_eof()
        if out_number != ans_number:
            raise InconsistentIntegersError(ans_number, out_number, out_file.line)
        result_file.report_ok('1 integer: ' % ans_number)
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    int_ocmp('stdin', sys.argv[2], 'stdout')
