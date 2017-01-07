# coding=utf-8
import json
import os
import _judger
from config import *
import languages


@celery.task
def _compile(lang, src_path, submission_id):
    output_dir = languages.get_exe_dir(submission_id)
    exe_path = languages.get_exe_path(lang, submission_id)
    command = languages.get_compile_command(lang, src_path, exe_path)
    compiler_out = os.path.join(output_dir, "compile.out")
    compiler_log = os.path.join(output_dir, "compile.log")
    _command = command.split(" ")

    result = _judger.run(max_cpu_time=languages.get_max_cpu_time(lang),
                         max_real_time=languages.get_max_real_time(lang),
                         max_memory=languages.get_max_memory(lang),
                         max_output_size=languages.get_max_output_size(lang),
                         max_process_number=_judger.UNLIMITED,
                         exe_path=_command[0],
                         # /dev/null is best, but in some system, this will call ioctl system call
                         input_path=src_path,
                         output_path=compiler_out,
                         error_path=compiler_out,
                         args=_command[1:],
                         env=[("PATH=" + os.getenv("PATH"))],
                         log_path=compiler_log,
                         seccomp_rule_name=None,
                         uid=0,
                         gid=0
                         )
    print(":::" + lang)
    print(result)
    if result["result"] != _judger.RESULT_SUCCESS:
        error_type = "re"
        if DEBUG:
            if os.path.exists(compiler_out):
                with open(compiler_out) as f:
                    error = f.read()
                    if error:
                        error_type = "ce"
                        print("Compile Error: " + error)
            if error_type == "re":
                print("Compiler Runtime Error: %s" % json.dumps(result))
        if not os.path.exists(compiler_out):
            with open(compiler_out, 'w') as f:
                f.write("Error Code="+result['error'])
        return False
    else:
        return True


def try_to_compile(submission):
    src_path = languages.get_src_path(submission['lang'], submission['id'])
    if os.path.exists(src_path):
        return True
    else:
        with open(src_path, 'w') as f:
            f.write(submission['code'])
        # TODO: running without celery
        return _compile(submission['lang'], src_path, str(submission['id']))