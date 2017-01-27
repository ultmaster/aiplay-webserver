# coding=utf-8
import shutil
from os import sys, path
import requests
import unittest

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from server import *

PROBLEM_ID = dict(
    a_plus_b=1000,
    a_mul_b=1001,
)

JSON_BASE_DICT = {"headers": {"Content-Type": "application/json"}}


class WebserverTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists('/judge_server'):
            shutil.rmtree('/judge_server')
        os.mkdir('/judge_server')
        os.mkdir('/judge_server/submission')
        os.mkdir('/judge_server/round')
        shutil.copytree(os.path.join(BASE_DIR, 'include'), INCLUDE_DIR)
        shutil.copytree(os.path.join(BASE_DIR, 'tests/test_data/data'), DATA_DIR)
        shutil.copytree(os.path.join(BASE_DIR, 'tests/test_data/pretest'), PRETEST_DIR)

    def tearDown(self):
        pass

    @staticmethod
    def send_pretest(data):
        kwargs = JSON_BASE_DICT.copy()
        kwargs["data"] = json.dumps(data)
        url = "http://127.0.0.1:4999/test"
        res = requests.post(url, json=data).json()
        print(json.dumps(res))
        return res

    @staticmethod
    def send_judge(data):
        kwargs = JSON_BASE_DICT.copy()
        kwargs["data"] = json.dumps(data)
        url = "http://127.0.0.1:4999/judge"
        res = requests.post(url, json=data).json()
        print(json.dumps(res))
        return res

    @staticmethod
    def formatSubmissionJSON(submission_id=0, lang='c', code_path=''):
        if '.' not in code_path:
            if lang == 'c':
                code_path += '.cpp'
            elif lang == 'p':
                code_path += '.py'
            elif lang == 'j':
                code_path += '.java'
        return {"id": submission_id, "lang": lang, "code": open('test_src/' + code_path, "r").read()}

    # A * B Problem Test

    def test_judge_a_mul_b_cpp(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(100, 'c', 'a_mul_b/a_mul_b_c_int'),
                self.formatSubmissionJSON(101, 'c', 'a_mul_b/a_mul_b_c_long')
            ],
            judge=self.formatSubmissionJSON(200, 'c', 'a_mul_b/a_mul_b_c_judge'),
            config={'problem_id': 1001}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], FINISHED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_judge_a_mul_b_python(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(100, 'c', 'a_mul_b/a_mul_b_c_int'),
                self.formatSubmissionJSON(101, 'c', 'a_mul_b/a_mul_b_c_long')
            ],
            judge=self.formatSubmissionJSON(201, 'p', 'a_mul_b/a_mul_b_p_judge'),
            config={'problem_id': 1001}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], FINISHED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_pretest_a_mul_b(self):
        data = dict(
            submission=self.formatSubmissionJSON(100, 'c', 'a_mul_b/a_mul_b_c_int'),
            judge=self.formatSubmissionJSON(201, 'p', 'a_mul_b/a_mul_b_p_judge'),
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    # Language Test

    def test_language_cpp(self):
        data = dict(
            submission={'id': 2000, 'lang': 'c', 'code': open('test_src/language/c.cpp').read()},
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_language_java(self):
        data = dict(
            submission={'id': 2001, 'lang': 'j', 'code': open('test_src/language/Main.java').read()},
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_language_python(self):
        data = dict(
            submission={'id': 2002, 'lang': 'p', 'code': open('test_src/language/p.py').read()},
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    # A + B Problem Test

    def test_judge_a_plus_b_ac(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(300, 'c', 'a_plus_b/a_plus_b_c_ok')
            ],
            judge=dict(id=205, lang='b', code='testlib/checker/int_ocmp.py'),
            config={'problem_id': 1000}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], FINISHED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_judge_a_plus_b_wa(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(301, 'c', 'a_plus_b/a_plus_b_c_wa')
            ],
            judge=dict(id=205, lang='b', code='testlib/checker/int_ocmp.py'),
            config={'problem_id': 1000}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], FINISHED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))


if __name__ == '__main__':
    unittest.main()
