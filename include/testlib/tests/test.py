import sys
import unittest
from os import path
from include.testlib.stream import InputStream
from include.testlib.exception import *

data_dir = path.join(path.dirname(path.abspath(__file__)), 'data')


class TestlibTest(unittest.TestCase):

    def test_read_all(self):
        ss = InputStream(path.join(data_dir, 'lines.txt'))
        ss.read_rest_of_file()
        self.assertEqual(ss.read_rest_of_file(), '')

    def test_read_line(self):
        ss = InputStream(path.join(data_dir, 'lines.txt'))
        ss.read_line()
        ss.read_line()
        with self.assertRaises(UnexpectedTokenInFileError):
            ss.read_eof()

    def test_read_token_and_eof(self):
        ss = InputStream(path.join(data_dir, 'lines.txt'))
        word_list = []
        for i in range(4):
            word_list.append(ss.read_word())
        print(word_list)
        ss.read_eof()
        with self.assertRaises(UnexpectedEOFError):
            ss.read_word()
        with self.assertRaises(UnexpectedEOFError):
            ss.read_line()

    def test_read_eol(self):
        ss = InputStream(path.join(data_dir, 'lines.txt'))
        ss.read_word()
        with self.assertRaises(UnexpectedTokenInLineError):
            ss.read_eol()

    def test_read_integer(self):
        ss = InputStream(path.join(data_dir, 'integers.txt'))
        integer_list = []
        for i in range(6):
            integer_list.append(ss.read_integer())
        print(integer_list)
        with self.assertRaises(UnexpectedTypeError):
            ss.read_integer()

    def test_read_real_number(self):
        ss = InputStream(path.join(data_dir, 'real_numbers.txt'))
        ss.read_real_number()


if __name__ == '__main__':
    unittest.main()
