# Compare two files, filtering out spaces at end-of-line and blank lines at end-of-file

from testlib import *


def file_cmp(out, ans, result):
    out_file = InputStream(out)
    ans_file = InputStream(ans)
    result_file = OutputStream(result)
    try:
        cnt = 0
        eof_expected = False
        eof_found = False
        ans_line = ''
        out_line = ''
        while True:
            try:
                ans_line = ans_file.read_line().rstrip()
            except UnexpectedEOFError:
                eof_expected = True
            except JudgeException:
                raise UnexpectedAnswerError(ans_file.line)
            try:
                out_line = out_file.read_line().rstrip()
            except UnexpectedEOFError:
                eof_found = True
            if eof_expected and eof_found:
                break
            if eof_expected and len(out_line) > 0:
                raise UnexpectedTokenInFileError(out_file.line)
            if eof_found and len(ans_line) > 0:
                raise UnexpectedEOFError(out_file.line)
            if ans_line != out_line:
                raise InconsistentTokensError(format_found_token(ans_line),
                                              format_found_token(out_line),
                                              out_file.line)
            cnt += 1
        result_file.report_ok('%d lines(s)' % cnt)
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    file_cmp('stdin', sys.argv[2], 'stdout')
