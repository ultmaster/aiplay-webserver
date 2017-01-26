# Compare two integers
# Keep doing that until End Of File

from testlib import *


def int_cmp(out, ans, result):
    out_file = InputStream(out)
    ans_file = InputStream(ans)
    result_file = OutputStream(result)
    try:
        cnt = 0
        eof_expected = False
        ans_number = 0
        while True:
            try:
                ans_number = ans_file.read_integer()
            except UnexpectedEOFError:
                eof_expected = True
            except JudgeException:
                raise UnexpectedAnswerError
            if eof_expected:
                out_file.read_eof()
                break
            else:
                out_number = out_file.read_integer()
            if out_number != ans_number:
                raise InconsistentIntegersError(ans_number, out_number, out_file.line)
            cnt += 1
        result_file.report_ok('%d integer(s)' % cnt)
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    int_cmp('stdin', sys.argv[2], 'stdout')
