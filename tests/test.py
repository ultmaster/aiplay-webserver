# coding=utf-8
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from compiler import _compile
import languages
import json
import unittest
import requests

cpp_src = """
#include <iostream>

using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a+b << endl;
    return 0;
}
"""

class WebserverTest(unittest.TestCase):

    def setup(self):
        pass

    def test_compile_directly(self):
        print(cpp_src)
        compile_config = languages.cpp_lang_config
        src_path = '/aiptest/test1.cpp'
        output_dir = '/aiptest'
        with open(src_path, "w") as f:
            f.write(cpp_src)
        _compile(compile_config, src_path, output_dir)

    def tearDown(self):
        pass



# class JudgeServerClientForTokenHeaderTest(JudgeServerClient):
#     def _request(self, url, data=None):
#         kwargs = {"headers": {"Content-Type": "application/json"}}
#         if data:
#             kwargs["data"] = json.dumps(data)
#         try:
#             return requests.post(url, **kwargs).json()
#         except Exception as e:
#             raise JudgeServerClientError(e.message)
#
#

if __name__ == '__main__':
    unittest.main()