import _judger
from config import *
from .languages import LANGUAGE_SETTINGS


# This class is meant to deal with all difficulties when it comes to programs.
# If initiated properly, you can simply use compile() and run() to run the program.
class Program(object):
    def __init__(self, submission, config):

        # About this program
        self.submission_id = submission['id']
        self.lang = submission['lang']
        self.code = submission['code']
        self.language_settings = LANGUAGE_SETTINGS[self.lang]
        self.score = 0
        self.sum_score = 0

        # Restrictive settings
        self.problem_id = config['problem_id']
        self.round_id = config['round_id']
        self.max_time = config['max_time']
        self.max_memory = config['max_memory']
        self.max_sum_time = config['max_sum_time']

        self.sum_time = 0
        # if you call it max, it is ok.
        self.sum_memory = 0

        # Deal with directories
        self.submission_dir = os.path.join(SUBMISSION_DIR, str(self.submission_id))
        self.round_dir = os.path.join(ROUND_DIR, str(self.round_id))
        if not os.path.exists(self.round_dir):
            os.mkdir(self.round_dir)
        if not os.path.exists(self.submission_dir):
            os.mkdir(self.submission_dir)

        # Ready to make some files
        self.src_name = self.language_settings['src_name']
        self.exe_name = self.language_settings['exe_name']
        self.src_path = os.path.join(self.submission_dir, self.src_name)
        self.exe_path = os.path.join(self.submission_dir, self.exe_name)

        # Compilation related
        self.compile_out_path = os.path.join(self.submission_dir, 'compile.out')
        self.compile_log_path = os.path.join(self.submission_dir, 'compile.log')
        self.compile_cmd = self.language_settings['compile_cmd'].format(
            src_path=self.src_path,
            exe_path=self.exe_path,
        ).split(' ')

        # Running related
        self.input_path = os.path.join(self.round_dir, 'in')
        self.output_path = os.path.join(self.round_dir, 'out')
        self.log_path = os.path.join(self.round_dir, 'run.log')
        self.seccomp_rule_name = self.language_settings['seccomp_rule']
        self.run_cmd = self.language_settings['exe_cmd'].format(
            exe_path=self.exe_path,
            # The following is for Java
            exe_dir=self.submission_dir,
            exe_name=self.exe_name,
            max_memory=self.max_memory
        ).split(' ')

    def compile(self):
        # TODO if compile result exist
        with open(self.src_path, 'w') as f:
            f.write(self.code)
        result = self._compile()
        print("Compile Result of " + self.lang + ": " + str(result))
        if result["result"] != _judger.RESULT_SUCCESS:
            if not os.path.exists(self.compile_out_path):
                with open(self.compile_out_path, 'w') as f:
                    f.write("Error Code = " + result['error'])
            return False
        return True

    def run(self):
        # Prevent input errors
        if not os.path.exists(self.input_path):
            open(self.input_path, "w").close()
        result = self._run()

        # Sum time
        self.sum_time += result['cpu_time']
        self.sum_memory = max(self.sum_memory, result['memory'])
        if self.max_sum_time > 0 and self.sum_time > self.max_sum_time:
            result['result'] = SUM_TIME_LIMIT_EXCEEDED

        # A fake one
        if result['result'] == CPU_TIME_LIMIT_EXCEEDED or result['result'] == REAL_TIME_LIMIT_EXCEEDED:
            result['time'] = self.max_time
        if result['result'] == MEMORY_LIMIT_EXCEEDED:
            result['memory'] = self.max_memory

        print("Running Result of " + self.lang + ": " + str(result))
        return result

    def _compile(self):
        return _judger.run(**self._compile_args())

    def _run(self):
        return _judger.run(**self._run_args())

    def _compile_args(self):
        return dict(
            max_cpu_time=30 * 1000,
            max_real_time=300 * 1000,
            max_memory=-1,
            max_output_size=128 * 1024 * 1024,
            max_process_number=_judger.UNLIMITED,
            exe_path=self.compile_cmd[0],
            # /dev/null is best, but in some system, this will call ioctl system call
            input_path=self.src_path,
            output_path=self.compile_out_path,
            error_path=self.compile_out_path,
            args=self.compile_cmd[1:],
            env=[("PATH=" + os.getenv("PATH"))] + self.language_settings['env'],
            log_path=self.compile_log_path,
            seccomp_rule_name=None,
            uid=0,
            gid=0
        )

    def _run_args(self):
        return dict(
            max_cpu_time=self.max_time,
            max_real_time=self.max_time * 10,
            max_memory=self.max_memory * 1048576 if self.lang != 'j' else -1,
            max_output_size=128 * 1024 * 1024,
            max_process_number=_judger.UNLIMITED,
            exe_path=self.run_cmd[0],
            input_path=self.input_path,
            output_path=self.output_path,
            error_path=self.log_path,
            args=self.run_cmd[1:],
            env=[("PATH=" + os.getenv("PATH"))] + self.language_settings['env'],
            log_path=self.log_path,
            seccomp_rule_name=self.seccomp_rule_name,
            uid=0,  # not safe
            gid=0
        )
