# coding=utf-8
from __future__ import unicode_literals
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import json
import unittest
import requests


class WebserverTest(unittest.TestCase):

    def setup(self):
        pass

    def test_compile(self):
        pass

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