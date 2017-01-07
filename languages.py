#coding=utf-8
LANGUAGE_SETTINGS = dict(
    c={
        "suffix_name": ".cpp",
        "exe_name": "main",
        "max_cpu_time": 15000,
        "max_real_time": 20000,
        "max_time_factor": 1,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++11 {src_path} -lm -o {exe_path}",
        "command": "{exe_path}",
        "seccomp_rule": "c_cpp"
    },
    j={
        "suffix_name": ".java",
        "exe_name": "Main",
        "max_cpu_time": 15000,
        "max_real_time": 20000,
        "max_memory": -1,
        "max_time_factor": 2,
        "compile_command": "/usr/bin/javac {src_path} -d {exe_dir} -encoding UTF8",
        "command": "/usr/bin/java -cp {exe_dir} -Xss1M -XX:MaxPermSize=16M -XX:PermSize=8M -Xms16M -Xmx{max_memory}k -Djava.security.manager -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main",
        "seccomp_rule": None,
        "env": ["MALLOC_ARENA_MAX=1"]
    },
    p={
        "suffix_name": ".py",
        "exe_name": "solution.pyc",
        "max_cpu_time": 15000,
        "max_real_time": 20000,
        "max_time_factor": 4,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/python3 -m py_compile {src_path}",
        "command": "/usr/bin/python {exe_path}",
        "seccomp_rule": None
    }
)