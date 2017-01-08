from languages import _LANGUAGE_SETTINGS
from config import COMPILE_DIR, SUBMISSION_DIR, DEBUG
import _judger
import os


class Program(object):
    def __init__(self, submission_config, round_config):
        self.submission_id = submission_config['id']
        self.lang = submission_config['lang']
        self._language_setting = _LANGUAGE_SETTINGS[self.lang]
        self._src_name = self._language_setting['src_name']
        self._exe_name = self._language_setting['exe_name']
        self.seccomp_rule = self._language_setting['seccomp_rule']
        self._max_time_factor = self._language_setting['max_time_factor']
        self.env = self._language_setting['env']

        self._code = submission_config['code']
        self.problem_id = round_config['problem_id']
        self.round_id = round_config['round_id']
        self.max_time = round_config['max_time'] * self._max_time_factor
        self.max_real_time = int(self.max_time * 1.2)
        self.max_sum_time = round_config['max_sum_time'] * self._max_time_factor
        self.max_memory = round_config['max_memory'] * (1048576 if self.lang != 'j' else 1024)

        self.submission_dir = os.path.join(SUBMISSION_DIR, str(self.submission_id))
        self.exe_path = os.path.join(self.submission_dir, self._exe_name)
        self.src_path = os.path.join(self.submission_dir, self._src_name)
        self.compile_cmd = self._language_setting['compile_cmd']\
            .format(src_path=self.src_path, exe_path=self.exe_path).split(' ')
        self.compile_out_path = os.path.join(self.submission_dir, 'compile.out')
        self.compile_log_path = os.path.join(self.submission_dir, 'compile.log')

    def _compile(self):
        print(self.compile_cmd[0])
        print(self.compile_cmd[1:])
        print([("PATH=" + os.getenv("PATH"))])
        os.mkdir(self.submission_dir)
        with open(self.src_path, 'w') as f:
            f.write(self._code)
        return _judger.run(max_cpu_time=self.max_time,
                           max_real_time=self.max_real_time,
                           max_memory=128 * 1024 * 1024,
                           max_output_size=128 * 1024 * 1024,
                           max_process_number=_judger.UNLIMITED,
                           exe_path=self.compile_cmd[0],
                           # /dev/null is best, but in some system, this will call ioctl system call
                           input_path=self.src_path,
                           output_path=self.compile_out_path,
                           error_path=self.compile_out_path,
                           args=self.compile_cmd[1:],
                           env=[("PATH=" + os.getenv("PATH"))],
                           log_path=self.compile_log_path,
                           seccomp_rule_name=None,
                           uid=0,
                           gid=0
                           )


class Submission(Program):
    def __init__(self, submission_config, round_config):
        super(Submission, self).__init__(submission_config, round_config)

    def compile(self):
        # TODO if compile result exist
        result = self._compile()
        print(":::" + self.lang)
        print(result)
        if result["result"] != _judger.RESULT_SUCCESS:
            if not os.path.exists(self.compile_out_path):
                with open(self.compile_out_path, 'w') as f:
                    f.write("Error Code=" + result['error'])
            return False
        else:
            return True




