# coding=utf-8
from os import sys, path
import requests
import os
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from core.compiler import _compile
from aipWebserver import *
import config
import languages
import unittest
import multiprocessing
import time

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

data = {
    "total_submissions": 2,
    "submissions": [
        {
            "id": 1000,
            "language": "c",
            "code": "int main(){}"
        },
        {
            "id": 1001,
            "language": "c",
            "code": "print('!')"
        }
    ],
    "judge": {
        "id": 200,
        "language": "j",
        "code": "class Main { public static void main() { } }"
    },
    "problem_id": 1001,
    "max_time": 1000,
    "max_sum_time": 10000,
    "max_memory": 256,
    "round_id": 1
}


class WebserverTest(unittest.TestCase):

    def setup(self):
        pass

    def test_compile_directly(self):
        compile_config = languages.LANGUAGE_SETTINGS['c']
        submission_id = 100
        src_path = os.path.join(config.SUBMISSION_DIR, str(submission_id) + ".cpp")
        with open(src_path, "w") as f:
            f.write(cpp_src)
        if DEBUG:
            _compile(compile_config, src_path, str(submission_id))
        else:
            _compile.delay(compile_config, src_path, str(submission_id))

    def test_compile_wrong_directly(self):
        compile_config = languages.LANGUAGE_SETTINGS['c']
        submission_id = 101
        src_path = os.path.join(config.SUBMISSION_DIR, str(submission_id) + ".cpp")
        with open(src_path, "w") as f:
            f.write(cpp_wrong_src)
        if DEBUG:
            _compile(compile_config, src_path, str(submission_id))
        else:
            _compile.delay(compile_config, src_path, str(submission_id))

    def test_myBackgroundtask(self):
        my_background_task.delay(20, 30)

    def tearDown(self):
        pass


class JudgeServerClientForTokenHeaderTest(unittest.TestCase):
    def test_request(self):
        kwargs = {"headers": {"Content-Type": "application/json"}}
        kwargs["data"] = json.dumps(data)
        url = "http://127.0.0.1:4999/"
        res = requests.post(url, json=data).json()
        print(json.dumps(res))
        return res



if __name__ == '__main__':
    unittest.main()