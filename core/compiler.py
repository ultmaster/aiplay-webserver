# coding=utf-8
import json
import os
from celery import Celery
import _judger
from config import *
from exception import CompileError


@celery.task
def _compile(compile_config, src_path, submission_id):
    output_dir = COMPILE_DIR
    command = compile_config["compile_command"]
    exe_path = os.path.join(output_dir, submission_id)
    command = command.format(src_path=src_path, exe_dir=output_dir, exe_path=exe_path)
    compiler_out = os.path.join(output_dir, submission_id + ".out")
    compiler_log_path = os.path.join(output_dir, submission_id + '.log')
    _command = command.split(" ")

    result = _judger.run(max_cpu_time=compile_config["max_cpu_time"],
                         max_real_time=compile_config["max_real_time"],
                         max_memory=compile_config["max_memory"],
                         max_output_size=1024 * 1024,
                         max_process_number=_judger.UNLIMITED,
                         exe_path=_command[0],
                         # /dev/null is best, but in some system, this will call ioctl system call
                         input_path=src_path,
                         output_path=compiler_out,
                         error_path=compiler_out,
                         args=_command[1:],
                         env=[("PATH=" + os.getenv("PATH"))],
                         log_path=compiler_log_path,
                         seccomp_rule_name=None,
                         uid=0,
                         gid=0
                         )

    print(result)
    if result["result"] != _judger.RESULT_SUCCESS:
        if os.path.exists(compiler_out):
            with open(compiler_out) as f:
                error = f.read()
                if error:
                    raise CompileError(error)
        raise CompileError("Compiler runtime error, info: %s" % json.dumps(result))

