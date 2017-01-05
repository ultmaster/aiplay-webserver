# coding=utf-8
from os import sys, path
import os
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from core.compiler import _compile
from aipWebserver import *
import config
import languages
import unittest

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

cpp_wrong_src = """
#include <iostream>

using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a+b << endl;
    return 0;
"""

class WebserverTest(unittest.TestCase):

    def setup(self):
        pass

    def test_compile_directly(self):
        compile_config = languages.cpp_lang_config
        submission_id = 100
        src_path = os.path.join(config.SUBMISSION_DIR, str(submission_id) + ".cpp")
        with open(src_path, "w") as f:
            f.write(cpp_src)
        _compile.delay(compile_config, src_path, str(submission_id))

    def test_compile_wrong_directly(self):
        compile_config = languages.cpp_lang_config
        submission_id = 101
        src_path = os.path.join(config.SUBMISSION_DIR, str(submission_id) + ".cpp")
        with open(src_path, "w") as f:
            f.write(cpp_wrong_src)
        _compile.delay(compile_config, src_path, str(submission_id))

    def test_myBackgroundtask(self):
        my_background_task.delay(20, 30)

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