# coding=utf-8
from celery import Celery
from flask import Flask

import grp
import os
import pwd
DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JUDGER_WORKSPACE_BASE = os.path.join(BASE_DIR, "judger_run")
LOG_BASE = os.path.join(BASE_DIR, "log")

SUBMISSION_DIR = '/judge_server/submission'
COMPILE_DIR = '/judge_server/compile'
ROUND_DIR = '/judge_server/round'
DATA_DIR = '/judge_server/data'

RUN_USER_UID = pwd.getpwnam("nobody").pw_uid
RUN_GROUP_GID = grp.getgrnam("nogroup").gr_gid

COMPILER_USER_UID = pwd.getpwnam("compiler").pw_uid
COMPILER_GROUP_GID = grp.getgrnam("compiler").gr_gid

TEST_CASE_DIR = "/test_case"
SPJ_SRC_DIR = "/spj"
SPJ_EXE_DIR = "/spj"

TOKEN_FILE_PATH = "/token.txt"

COMPILE_ERROR = -2
WRONG_ANSWER = -1
CPU_TIME_LIMIT_EXCEEDED = 1
REAL_TIME_LIMIT_EXCEEDED = 2
MEMORY_LIMIT_EXCEEDED = 3
RUNTIME_ERROR = 4
SYSTEM_ERROR = 5

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_IMPORTS'] = ['core.compiler', 'aipWebserver']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
