from config import SUBMISSION_DIR, COMPILE_DIR
import os


LANGUAGE_SETTINGS = dict(
    c = {
        "src_name": "main.cpp",
        "exe_name": "main",
        "max_memory": 128 * 1024 * 1024,
        "compile_cmd": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++11 {src_path} -lm -o {exe_path}",
        "exe_cmd": "{exe_path}",
        "seccomp_rule": "c_cpp",
        "env": []
    },
    j = {
        "src_name": "Main.java",
        "exe_name": "Main",
        "max_memory": -1,
        "compile_cmd": "/usr/bin/javac {src_path} -encoding UTF8",
        "exe_cmd": "/usr/bin/java -cp {exe_dir} {exe_name} -Xss1M -XX:MaxPermSize=16M -XX:PermSize=8M -Xms16M -Xmx{max_memory}M -Djava.security.manager -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main",
        "seccomp_rule": None,
        "env": ["MALLOC_ARENA_MAX=1"]
    },
    p = {
        # A Naive solution of copy
        "src_name": "solution.py",
        "exe_name": "solution.py",  # TODO assign exe_path when compile
        "max_memory": 128 * 1024 * 1024,
        "compile_cmd": "/usr/bin/python3 -m py_compile {src_path}",
        "exe_cmd": "/usr/bin/python3 {exe_path}",
        "seccomp_rule": None,
        "env": []
    }
)


