# coding=utf-8
from os import sys, path
import shutil
import requests
import os
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from core.compiler import try_to_compile
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
  "total_submissions":2,
  "submissions":[
    {
      "id":100,
      "lang":"c",
      "code":"int main(){}"
    },
    {
      "id":101,
      "lang":"p",
      "code":"print('!')"
    }
  ],
  "judge": {
    "id":200,
    "lang":"j",
    "code":"class Main { public static void main() { } }"
  },
  "round_config": {
    "problem_id":1001,
    "max_time":1000,
    "max_sum_time":10000,
    "max_memory":256,
    "round_id":1
  }
}


class WebserverTest(unittest.TestCase):

    def setUp(self):
        shutil.rmtree('/aipWebserver')
        os.mkdir('/aipWebserver')
        os.mkdir('/aipWebserver/submission')
        os.mkdir('/aipWebserver/round')
        os.mkdir('/aipWebserver/data')
        os.mkdir('/aipWebserver/data/1001')
        os.mkdir('/aipWebserver/compile')

    # def test_compile_directly(self):
    #     submission = dict()
    #     submission["id"] = 100
    #     submission["lang"] = 'c'
    #     submission["code"] = cpp_src
    #     try_to_compile(submission)
    #
    # def test_compile_wrong_directly(self):
    #     submission = dict()
    #     submission["id"] = 101
    #     submission["lang"] = 'c'
    #     submission["code"] = cpp_wrong_src
    #     try_to_compile(submission)

    def tearDown(self):
        pass

    def test_request(self):
        kwargs = {"headers": {"Content-Type": "application/json"}}
        kwargs["data"] = json.dumps(data)
        url = "http://127.0.0.1:4999/"
        res = requests.post(url, json=data).json()
        print(json.dumps(res))
        # return res

if __name__ == '__main__':
    unittest.main()