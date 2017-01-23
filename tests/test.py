# coding=utf-8
import shutil
from os import sys, path

import requests

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from server import *
import unittest

# Correct A+B
cpp_src_1 = """
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

# Compile Error A+B
cpp_src_2 = """
#include <iostream>
using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a+b << endl;
    return 0;
"""

# Wrong Answer A+B
cpp_src_3 = """
#include <iostream>
using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a+b+1 << endl;
    return 0;
}
"""

# Wrong A*B
cpp_src_4 = """
#include <iostream>
using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a*b << endl;
    return 0;
}
"""

# Correct A*B
cpp_src_5 = """
#include <iostream>
using namespace std;

int main()
{
    long long a,b;
    cin >> a >> b;
    cout << a*b << endl;
    return 0;
}
"""

# A*B JUDGER
cpp_src_6 = """
#include <bits/stdc++.h>
using namespace std;

int main()
{
    ifstream fin("judge_in");
    long long a,b,c;
    fin >> a >> b;
    cin >> c;
    if (a * b == c)
        cout << "wrong answer" << endl;
    else cout << "ok" << endl;
    return 0;
}
"""

data = {
  "submissions":[
    {
      "id":100,
      "lang":"c",
      "code":cpp_src_4
    },
    {
      "id":101,
      "lang":"c",
      "code":cpp_src_5
    }
  ],
  "judge": {
    "id":200,
    "lang":"j",
    "code":"class Main { public static void main(String[] args) { } }"
  },
  "config": {
    "problem_id":1001,
    "round_id":1,
    "max_time":1000,
    "max_sum_time":10000,
    "max_memory":256
  }
}


class WebserverTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists('/judge_server'):
            shutil.rmtree('/judge_server')
        os.mkdir('/judge_server')
        os.mkdir('/judge_server/submission')
        os.mkdir('/judge_server/round')
        os.mkdir('/judge_server/data')
        os.mkdir('/judge_server/data/1001')


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
        url = "http://127.0.0.1:4999/judge"
        res = requests.post(url, json=data).json()
        print(json.dumps(res))
        # return res


if __name__ == '__main__':
    unittest.main()