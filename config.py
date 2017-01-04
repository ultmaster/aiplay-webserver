# coding=utf-8
from __future__ import unicode_literals

import grp
import os
import pwd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JUDGER_WORKSPACE_BASE = os.path.join(BASE_DIR, "judger_run")
LOG_BASE = os.path.join(BASE_DIR, "log")

COMPILER_LOG_PATH = os.path.join(LOG_BASE, "compile.log")
JUDGER_RUN_LOG_PATH = os.path.join(LOG_BASE, "judger.log")

RUN_USER_UID = pwd.getpwnam("nobody").pw_uid
RUN_GROUP_GID = grp.getgrnam("nogroup").gr_gid

# COMPILER_USER_UID = pwd.getpwnam("compiler").pw_uid
# COMPILER_GROUP_GID = grp.getgrnam("compiler").gr_gid

TEST_CASE_DIR = "/test_case"
SPJ_SRC_DIR = "/spj"
SPJ_EXE_DIR = "/spj"

TOKEN_FILE_PATH = "/token.txt"