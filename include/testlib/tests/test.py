import unittest
from os import path

from testlib import *
from testlib.checker import float_cmp, float_ocmp, float_ncmp
from testlib.checker import int_cmp, int_ocmp, int_ncmp
from testlib.checker import file_cmp

data_dir = path.join(path.dirname(path.abspath(__file__)), 'data')
res_path = path.join(data_dir, 'test.log')

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
        with self.assertRaises(UnexpectedTypeError):
            ss.read_integer()

    def test_read_real_number(self):
        ss = InputStream(path.join(data_dir, 'real_numbers.txt'))
        ss.read_real_number()

    def test_float_cmp(self):
        float_cmp.float_cmp(path.join(data_dir, 'float_cmp.out'), path.join(data_dir, 'float_cmp.ans'), res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'^ok')

    def test_float_cmp_eof_1(self):
        float_cmp.float_cmp(path.join(data_dir, 'float_cmp_less.out'), path.join(data_dir, 'float_cmp.ans'), res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'^idleness')
        self.assertRegex(res, r'eof found')

    def test_float_cmp_eof_2(self):
        float_cmp.float_cmp(path.join(data_dir, 'float_cmp_more.out'), path.join(data_dir, 'float_cmp.ans'), res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'^idleness')
        self.assertRegex(res, r'another token found')

    def test_float_cmp_not_float(self):
        float_cmp.float_cmp(path.join(data_dir, 'float_cmp_not_float.out'), path.join(data_dir, 'float_cmp.ans'), res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'^idleness')
        self.assertRegex(res, r'a real number expected')

    def test_float_cmp_wrong(self):
        float_cmp.float_cmp(path.join(data_dir, 'float_cmp_wrong.out'), path.join(data_dir, 'float_cmp.ans'),
                            res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'^wrong')

    def test_float_cmp_answer_wrong(self):
        float_cmp.float_cmp(path.join(data_dir, 'float_cmp.out'), path.join(data_dir, 'float_cmp_wrong.ans'),
                            res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'illegal')

    def test_float_ocmp(self):
        float_ocmp.float_ocmp(path.join(data_dir, 'float_ocmp.out'), path.join(data_dir, 'float_ocmp.ans'),
                            res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'^ok')

    def test_float_ncmp(self):
        float_ncmp.float_ncmp(path.join(data_dir, 'float_ncmp.out'), path.join(data_dir, 'float_ncmp.ans'),
                            res_path)
        res = open(res_path).readline()
        print(res)
        self.assertRegex(res, r'^wrong')

    def test_int_cmp(self):
        int_ocmp.int_ocmp(path.join(data_dir, 'int_cmp.out'), path.join(data_dir, 'int_cmp.ans'), res_path)
        self.assertRegex(open(res_path).readline(), r'^wrong')
        int_ncmp.int_ncmp(path.join(data_dir, 'int_ncmp.out'), path.join(data_dir, 'int_ncmp.ans'), res_path)
        self.assertRegex(open(res_path).readline(), r'^ok')
        int_cmp.int_cmp(path.join(data_dir, 'int_ncmp.out'), path.join(data_dir, 'int_ncmp.ans'), res_path)
        self.assertRegex(open(res_path).readline(), r'^ok')

    def test_file_cmp(self):
        file_cmp.file_cmp(path.join(data_dir, 'file_cmp.out'), path.join(data_dir, 'file_cmp.ans'), res_path)
        self.assertRegex(open(res_path).readline(), r'^ok')

if __name__ == '__main__':
    unittest.main()
