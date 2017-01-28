# coding=utf-8
from celery import Celery
from flask import Flask

import grp
import os
import pwd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JUDGE_BASE_DIR = '/judge_server'
JUDGE_BASE_DIR_PAST = '/judge_server_past'

SUBMISSION_DIR = os.path.join(JUDGE_BASE_DIR, 'submission')
COMPILE_DIR = os.path.join(JUDGE_BASE_DIR, 'compile')
ROUND_DIR = os.path.join(JUDGE_BASE_DIR, 'round')
DATA_DIR = os.path.join(JUDGE_BASE_DIR, 'data')
PRETEST_DIR = os.path.join(JUDGE_BASE_DIR, 'pretest')
INCLUDE_DIR = os.path.join(JUDGE_BASE_DIR, 'include')

RUN_USER_UID = pwd.getpwnam("nobody").pw_uid
RUN_GROUP_GID = grp.getgrnam("nogroup").gr_gid

COMPILER_USER_UID = pwd.getpwnam("compiler").pw_uid
COMPILER_GROUP_GID = grp.getgrnam("compiler").gr_gid

TOKEN_FILE_PATH = os.path.join(JUDGE_BASE_DIR, 'token')

# ERROR_CODE < 0: FORGIVEN
FINISHED = -100
CORRECT = -3
OK = -2
WRONG_ANSWER = -1

PRETEST_PASSED = 0

# ERROR_CODE > 0: TERMINATION ERROR
CPU_TIME_LIMIT_EXCEEDED = 1
REAL_TIME_LIMIT_EXCEEDED = 2
MEMORY_LIMIT_EXCEEDED = 3
RUNTIME_ERROR = 4
SYSTEM_ERROR = 5
COMPILE_ERROR = 6
IDLENESS_LIMIT_EXCEEDED = 7
PRETEST_FAILED = 8
SUM_TIME_LIMIT_EXCEEDED = 9

ERROR_CODE = {
    -100: 'Finished',
    -3: 'Correct',
    -2: 'OK',
    -1: 'Wrong Answer',
    0: 'Pretest Passed',
    1: 'Time Limit Exceeded',
    2: 'Time Limit Exceeded',
    3: 'Memory Limit Exceeded',
    4: 'Runtime Error',
    5: 'System Error',
    6: 'Compile Error',
    7: 'Idleness Limit Exceeded',
    8: 'Pretest Failed',
    9: 'Sum Time Limit Exceeded'
}

# For using built-in judge
BUILTIN_JUDGE = -1

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_IMPORTS'] = ['core.program']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
