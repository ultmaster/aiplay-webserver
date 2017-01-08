from config import *
from languages import Language
import _judger

def _runner(lang):
    result = _judger.run(max_cpu_time=lang.get_max_cpu_time(),
                         max_real_time=lang.get_max_real_time(),
                         max_memory=lang.get_max_memory(),
                         max_output_size=lang.get_max_output_size(lang),
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
