# Compare two sequences of words
# Keep doing that until End Of File

from testlib import *


def word_cmp(out, ans, result):
    out_file = InputStream(out)
    ans_file = InputStream(ans)
    result_file = OutputStream(result)
    try:
        cnt = 0
        eof_expected = False
        ans_word = ''
        while True:
            try:
                ans_word = ans_file.read_word()
            except UnexpectedEOFError:
                eof_expected = True
            except JudgeException:
                raise UnexpectedAnswerError(ans_file.line)
            if eof_expected:
                out_file.read_eof()
                break
            else:
                out_word = out_file.read_word()
            if ans_word != out_word:
                raise InconsistentTokensError(ans_word, out_word, out_file.line)
            cnt += 1
        result_file.report_ok('%d word(s)' % cnt)
    except JudgeException as e:
        result_file.writeline(e)

if __name__ == '__main__':
    word_cmp('stdin', sys.argv[2], 'stdout')
