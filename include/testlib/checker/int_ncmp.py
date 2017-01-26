# Compare two real integer lists
# Start with length of list, and then integers follow

from testlib import *


def int_ncmp(out, ans, result):
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
                ans_number = ans_file.read_integer()
            except JudgeException:
                raise UnexpectedAnswerError
            out_number = out_file.read_integer()
            if out_number != ans_number:
                raise InconsistentIntegersError(ans_number, out_number, out_file.line)
        try:
            ans_file.read_eof()
        except JudgeException:
            raise UnexpectedAnswerError
        out_file.read_eof()
        result_file.report_ok('%d integer(s)' % ans_length)
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    int_ncmp('stdin', sys.argv[2], 'stdout')
