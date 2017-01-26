# coding=utf-8
import shutil
from os import sys, path

import requests

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from server import *
from core.program import Program
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
#include <testlib/test.h>
using namespace std;

int main(int argc, char **argv)
{
    ifstream fin(argv[1]);
    ofstream fout(argv[3]);
    long long a,b,c;
    fin >> a >> b;
    cin >> c;
    if (a * b != c)
        cout << "stop, wrong answer" << endl;
    else {
        cout << "continue, ok" << endl;
        fout << c << " " << c - 1 << endl;
        fout.close();
    }
    return 0;
}
"""

# A*B Judger Python
python_src_1 = """
import os, sys, testlib
newin = open(sys.argv[3], 'w')
oldin = open(sys.argv[1], 'r')
a, b = map(int, oldin.readline().split())
c = int(input())
if a * b != c:
    print('stop, wrong answer')
else:
    print('continue, ok')
    newin.write("%d %d\\n" % (c, c - 1))
"""

data_1 = {
    "submission":{
        "id":104,
        "lang":"c",
        "code":cpp_src_3
    },
    "judge": {
        "id":200,
        "lang":"c",
        "code":cpp_src_6
    },
    "config": {
        "problem_id":1001,
        "max_time":1000,
        "max_sum_time":10000,
        "max_memory":256
    }
}

data_2 = {
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
    "id":201,
    "lang":"p",
    "code":python_src_1
  },
  "config": {
    "problem_id":1001,
    "max_time":1000,
    "max_sum_time":10000,
    "max_memory":256
  }
}

data_3 = {
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
    "lang":"c",
    "code":cpp_src_6
  },
  "config": {
    "problem_id":1001,
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
        shutil.copytree(os.path.join(BASE_DIR, 'include'), INCLUDE_DIR)
        os.mkdir('/judge_server/submission')
        os.mkdir('/judge_server/round')
        os.mkdir('/judge_server/data')
        os.mkdir('/judge_server/data/1001')
        with open('/judge_server/data/1001/input.txt', 'w') as f:
            f.write('3 2')
        os.mkdir('/judge_server/pretest')
        os.mkdir('/judge_server/pretest/1001')
        with open('/judge_server/pretest/1001/input1.txt', 'w') as f:
            f.write('3 2')

    def tearDown(self):
        pass

    def send_pretest(self, data):
        kwargs = {"headers": {"Content-Type": "application/json"}}
        kwargs["data"] = json.dumps(data_1)
        url = "http://127.0.0.1:4999/test"
        res = requests.post(url, json=data).json()
        print(json.dumps(res))
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed. ' + json.dumps(res))

    def test_judge_cpp(self):
        self.send_judge(data_3)

    def test_judge_python(self):
        self.send_judge(data_2)

    def send_judge(self, data):
        kwargs = {"headers": {"Content-Type": "application/json"}}
        kwargs["data"] = json.dumps(data_2)
        url = "http://127.0.0.1:4999/judge"
        res = requests.post(url, json=data_2).json()
        print(json.dumps(res))
        self.assertEqual(res['code'], FINISHED, json.dumps(res))
        for score in res['score'].values():
            self.assertGreaterEqual(score, 20, 'Basic Test Judge Failed. ' + json.dumps(res))

    def test_pretest(self):
        self.send_pretest(data_1)

    def test_language_cpp(self):
        data = dict(
            submission={'id': 2000, 'lang': 'c', 'code': open('test_src/language/c.cpp').read()},
            config={'problem_id': 1001}
        )
        self.send_pretest(data)

    def test_language_java(self):
        data = dict(
            submission={'id': 2001, 'lang': 'j', 'code': open('test_src/language/Main.java').read()},
            config={'problem_id': 1001}
        )
        self.send_pretest(data)

    def test_language_python(self):
        data = dict(
            submission={'id': 2002, 'lang': 'p', 'code': open('test_src/language/p.py').read()},
            config={'problem_id': 1001}
        )
        self.send_pretest(data)

if __name__ == '__main__':
    unittest.main()