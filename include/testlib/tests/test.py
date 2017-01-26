import sys
import unittest
from os import path
from include.testlib.stream import InputStream

data_dir = path.join(path.dirname(path.abspath(__file__)), 'data')


class TestlibTest(unittest.TestCase):

    def test_read_all(self):
        ss = InputStream(path.join(data_dir, 'lines.txt'))
        self.assertGreater(len(ss.read_all()), 0)


if __name__ == '__main__':
    unittest.main()
