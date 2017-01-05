# coding=utf-8
from celery import Celery
from flask import Flask

import grp
import os
import pwd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JUDGER_WORKSPACE_BASE = os.path.join(BASE_DIR, "judger_run")
LOG_BASE = os.path.join(BASE_DIR, "log")

SUBMISSION_DIR = '/aipWebserver/submission'
COMPILE_DIR = '/aipWebserver/compile'

RUN_USER_UID = pwd.getpwnam("nobody").pw_uid
RUN_GROUP_GID = grp.getgrnam("nogroup").gr_gid

COMPILER_USER_UID = pwd.getpwnam("compiler").pw_uid
COMPILER_GROUP_GID = grp.getgrnam("compiler").gr_gid

TEST_CASE_DIR = "/test_case"
SPJ_SRC_DIR = "/spj"
SPJ_EXE_DIR = "/spj"

TOKEN_FILE_PATH = "/token.txt"

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_IMPORTS'] = ['core.compiler', 'aipWebserver']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
