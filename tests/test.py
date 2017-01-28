# coding=utf-8
import shutil
from os import sys, path
import requests
import json
from requests.auth import HTTPBasicAuth
import unittest
import zipfile

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from server import *

PROBLEM_ID = dict(
    a_plus_b=1000,
    a_mul_b=1001,
)

JSON_BASE_DICT = {"headers": {"Content-Type": "application/json"}}


class WebserverTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists(JUDGE_BASE_DIR):
            shutil.rmtree(JUDGE_BASE_DIR)
        os.mkdir(JUDGE_BASE_DIR)
        os.mkdir(SUBMISSION_DIR)
        os.mkdir(ROUND_DIR)
        os.mkdir(TMP_DIR)
        with open(TOKEN_FILE_PATH, 'w') as f:
            f.write('token')
        shutil.copytree(os.path.join(BASE_DIR, 'include'), INCLUDE_DIR)
        shutil.copytree(os.path.join(BASE_DIR, 'tests/test_data/data'), DATA_DIR)
        shutil.copytree(os.path.join(BASE_DIR, 'tests/test_data/pretest'), PRETEST_DIR)

        # Java problem
        os.chown(os.path.join(INCLUDE_DIR, 'testlib/include_test'), COMPILER_USER_UID, COMPILER_GROUP_GID)
        with open('/etc/java_policy', 'w') as f:
            f.write(open('java_policy').read())

    def tearDown(self):
        pass

    @staticmethod
    def send_pretest(data):
        kwargs = JSON_BASE_DICT.copy()
        kwargs["data"] = json.dumps(data)
        url = "http://127.0.0.1:4999/test"
        res = requests.post(url, json=data, auth=('token', 'token')).json()
        print(json.dumps(res))
        return res

    @staticmethod
    def send_judge(data):
        kwargs = JSON_BASE_DICT.copy()
        kwargs["data"] = json.dumps(data)
        url = "http://127.0.0.1:4999/judge"
        res = requests.post(url, json=data, auth=('token', 'token')).json()
        print(json.dumps(res))
        return res

    @staticmethod
    def formatSubmissionJSON(submission_id=0, lang='cpp', code_path=''):
        if '.' not in code_path:
            if lang == 'cpp':
                code_path += '.cpp'
            elif lang == 'python':
                code_path += '.py'
            elif lang == 'java':
                code_path += '.java'
        return {"id": submission_id, "lang": lang, "code": open('test_src/' + code_path, "r").read()}

    @staticmethod
    def add_dir_to_file(omitted_dir, source_dir, target_path):
        f = zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED)
        dir = os.path.join(omitted_dir, source_dir)
        for dir_path, dir_names, file_names in os.walk(dir):
            for filename in file_names:
                file_real_path = os.path.join(dir_path, filename)
                f.write(file_real_path, arcname=os.path.relpath(file_real_path, omitted_dir))
        f.close()

    def test_upload(self):
        url = "http://127.0.0.1:4999/upload"
        self.add_dir_to_file('test_data', 'data/1002', 'test_data/upload.zip')
        with open('test_data/upload.zip', 'rb') as f:
            res = requests.post(url, data=f, auth=('token', 'token')).json()
            print(json.dumps(res))
            return res

    # A * B Problem Test

    def test_judge_a_mul_b_cpp(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(100, 'cpp', 'a_mul_b/a_mul_b_c_int'),
                self.formatSubmissionJSON(101, 'cpp', 'a_mul_b/a_mul_b_c_long')
            ],
            judge=self.formatSubmissionJSON(200, 'cpp', 'a_mul_b/a_mul_b_c_judge'),
            config={'problem_id': 1001}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], FINISHED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_judge_a_mul_b_python(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(100, 'cpp', 'a_mul_b/a_mul_b_c_int'),
                self.formatSubmissionJSON(101, 'cpp', 'a_mul_b/a_mul_b_c_long')
            ],
            judge=self.formatSubmissionJSON(201, 'python', 'a_mul_b/a_mul_b_p_judge'),
            config={'problem_id': 1001}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], FINISHED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_pretest_a_mul_b(self):
        data = dict(
            submission=self.formatSubmissionJSON(100, 'cpp', 'a_mul_b/a_mul_b_c_int'),
            judge=self.formatSubmissionJSON(201, 'python', 'a_mul_b/a_mul_b_p_judge'),
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    # Language Test

    def test_language_cpp(self):
        data = dict(
            submission={'id': 2000, 'lang': 'cpp', 'code': open('test_src/language/c.cpp').read()},
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_language_java(self):
        data = dict(
            submission={'id': 2001, 'lang': 'java', 'code': open('test_src/language/Main.java').read()},
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_language_python(self):
        data = dict(
            submission={'id': 2002, 'lang': 'python', 'code': open('test_src/language/p.py').read()},
            config={'problem_id': 1001}
        )
        res = self.send_pretest(data)
        self.assertEqual(res['code'], PRETEST_PASSED, 'Pretest Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    # A + B Problem Test

    def test_judge_a_plus_b_ac(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(300, 'cpp', 'a_plus_b/a_plus_b_c_ok')
            ],
            judge=dict(lang='builtin', code='testlib/checker/int_ocmp.py'),
            config={'problem_id': 1000}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], FINISHED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))

    def test_judge_a_plus_b_wa(self):
        data = dict(
            submissions=[
                self.formatSubmissionJSON(301, 'cpp', 'a_plus_b/a_plus_b_c_wa')
            ],
            pretest_judge=dict(lang='builtin', code='testlib/checker/int_ocmp.py'),
            judge=dict(lang='builtin', code='testlib/checker/int_ocmp.py'),
            config={'problem_id': 1000}
        )
        res = self.send_judge(data)
        self.assertEqual(res['code'], PRETEST_FAILED, 'Judge Failed for REASON: %s; JSON: %s'
                         % (ERROR_CODE[res['code']], json.dumps(res)))


if __name__ == '__main__':
    unittest.main()
