#coding=utf-8

from config import SUBMISSION_DIR, COMPILE_DIR
import os

_LANGUAGE_SETTINGS = dict(
    c = {
        "src_name": "main.cpp",
        "exe_name": "main",
        "max_time_factor": 1,
        "max_memory": 128 * 1024 * 1024,
        "compile_cmd": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++11 {src_path} -lm -o {exe_path}",
        "exe_cmd": "{exe_path}",
        "seccomp_rule": "c_cpp",
        "env": []
    },
    j = {
        "src_name": "Main.java",
        "exe_name": "Main",
        "max_time_factor": 2,
        "max_memory": -1,
        "compile_cmd": "/usr/bin/javac {src_path} -d {exe_path} -encoding UTF8",
        "exe_cmd": "/usr/bin/java -cp {exe_path} -Xss1M -XX:MaxPermSize=16M -XX:PermSize=8M -Xms16M -Xmx{max_memory}k -Djava.security.manager -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main",
        "seccomp_rule": None,
        "env": ["MALLOC_ARENA_MAX=1"]
    },
    p = {
        # A Naive solution of copy
        "src_name": "solution.py",
        "exe_name": "solution.pyc",
        "max_time_factor": 4,
        "max_memory": 128 * 1024 * 1024,
        "compile_cmd": "/usr/bin/python3 -m py_compile {src_path}",
        "exe_cmd": "/usr/bin/python3 {exe_path}",
        "seccomp_rule": None,
        "env": []
    }
)

def get_source_name(lang):
    return _LANGUAGE_SETTINGS[lang]["source_name"]

def get_exe_name(lang):
    return _LANGUAGE_SETTINGS[lang]["exe_name"]

def get_max_cpu_time(lang, time_limit=-1):
    _time = time_limit
    if _time == -1:
        _time = 15000
    _time *= _LANGUAGE_SETTINGS[lang]["max_time_factor"]
    return _time

def get_max_real_time(lang, time_limit=-1):
    return int(get_max_cpu_time(lang, time_limit) * 1.2)

def get_max_output_size(lang):
    return 1024 * 1024 * 10

def get_max_memory(lang, memory_limit=-1):
    if memory_limit == -1:
        return _LANGUAGE_SETTINGS[lang]["max_memory"]
    else:
        return memory_limit

def get_compile_command(lang, src_path, exe_path):
    if lang == 'j':
        _exe_path = os.path.dirname(exe_path)
    else:
        _exe_path = exe_path
    return _LANGUAGE_SETTINGS[lang]["compile_command"].format(src_path=src_path, exe_path=_exe_path)

def get_run_command(lang, exe_path, memory_limit=0):
    # Memory Limit Required for Java
    if lang == 'j' and memory_limit == 0:
        raise ValueError("Memory Limit required for Java Running")
    return _LANGUAGE_SETTINGS[lang]["command"].format(exe_path=exe_path, max_memory=memory_limit)

def get_seccomp_rule(lang):
    return _LANGUAGE_SETTINGS[lang]["seccomp_rule"]

def get_additional_env(lang):
    return _LANGUAGE_SETTINGS[lang]["env"]

def get_src_path(lang, submission_id):
    src_dir = os.path.join(SUBMISSION_DIR, str(submission_id))
    src_path = os.path.join(src_dir, get_source_name(lang))
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)
    return src_path

def get_exe_dir(submission_id):
    exe_dir = os.path.join(COMPILE_DIR, str(submission_id))
    if not os.path.exists(exe_dir):
        print("!!!" + exe_dir)
        os.mkdir(exe_dir)
    return exe_dir

def get_exe_path(lang, submission_id):
    return os.path.join(get_exe_dir(submission_id), get_exe_name(lang))
