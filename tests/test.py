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
import os, sys
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

    def test_pretest(self):
        kwargs = {"headers": {"Content-Type": "application/json"}}
        kwargs["data"] = json.dumps(data_1)
        url = "http://127.0.0.1:4999/test"
        res = requests.post(url, json=data_1).json()
        print(json.dumps(res))

    def test_judge(self):
        kwargs = {"headers": {"Content-Type": "application/json"}}
        kwargs["data"] = json.dumps(data_2)
        url = "http://127.0.0.1:4999/judge"
        res = requests.post(url, json=data_2).json()
        print(json.dumps(res))


if __name__ == '__main__':
    unittest.main()