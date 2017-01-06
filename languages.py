#coding=utf-8
LANGUAGE_SETTINGS = dict(
    c={
        "src_name": "main.cpp",
        "exe_name": "main",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++11 {src_path} -lm -o {exe_path}",
        "command": "{exe_path}",
        "seccomp_rule": "c_cpp"
    },
    j={
        "name": "java",
        "compile": {
            "src_name": "Main.java",
            "exe_name": "Main",
            "max_cpu_time": 3000,
            "max_real_time": 5000,
            "max_memory": -1,
            "compile_command": "/usr/bin/javac {src_path} -d {exe_dir} -encoding UTF8"
        },
        "run": {
            "command": "/usr/bin/java -cp {exe_dir} -Xss1M -XX:MaxPermSize=16M -XX:PermSize=8M -Xms16M -Xmx{max_memory}k -Djava.security.manager -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main",
            "seccomp_rule": None,
            "env": ["MALLOC_ARENA_MAX=1"]
        }
    },

    py2_lang_config={
        "compile": {
            "src_name": "solution.py",
            "exe_name": "solution.pyc",
            "max_cpu_time": 3000,
            "max_real_time": 5000,
            "max_memory": 128 * 1024 * 1024,
            "compile_command": "/usr/bin/python -m py_compile {src_path}",
        },
        "run": {
            "command": "/usr/bin/python {exe_path}",
            "seccomp_rule": None,
        }
    }
)