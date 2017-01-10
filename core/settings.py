import os
from languages import _LANGUAGE_SETTINGS
import _judger
from config import *


class BaseSettings(object):
    def __init__(self, submission_config, round_config):
        self.submission_id = submission_config['id']
        self.lang = submission_config['lang']
        self.code = submission_config['code']

        self.language_settings = _LANGUAGE_SETTINGS[self.lang]

        self.problem_id = round_config['problem_id']
        self.round_id = round_config['round_id']
        self.max_time = round_config['max_time']
        self.max_memory = round_config['max_memory']


class CompileSettings(object):
    def __init__(self, settings):
        self.submission_dir = os.path.join(SUBMISSION_DIR, str(settings.submission_id))
        self.src_name = settings.language_settings['src_name']
        self.exe_name = settings.language_settings['exe_name']
        self.src_path = os.path.join(self.submission_dir, self.src_name)
        self.exe_path = os.path.join(self.submission_dir, self.exe_name)
        self.compile_out_path = os.path.join(self.submission_dir, 'compile.out')
        self.compile_log_path = os.path.join(self.submission_dir, 'compile.log')
        self.compile_cmd = settings.language_settings['compile_cmd'].format(
            src_path=self.src_path,
            exe_path=self.exe_path,
        ).split(' ')
        self.compile = dict(
            max_cpu_time=20 * 1000,
            max_real_time=20 * 1000,
            max_memory=128 * 1024 * 1024 if settings.lang != 'j' else -1,
            max_output_size=128 * 1024 * 1024,
            max_process_number=_judger.UNLIMITED,
            exe_path=self.compile_cmd[0],
            # /dev/null is best, but in some system, this will call ioctl system call
            input_path=self.src_path,
            output_path=self.compile_out_path,
            error_path=self.compile_out_path,
            args=self.compile_cmd[1:],
            env=[("PATH=" + os.getenv("PATH"))] + settings.language_settings['env'],
            log_path=self.compile_log_path,
            seccomp_rule_name=None,
            uid=0,
            gid=0
        )


class RunSettings(object):
    def __init__(self, settings):
        self.round_dir = os.path.join(ROUND_DIR, str(settings.submission_id))
        self.exe_name = settings.language_settings['exe_name']
        self.exe_path = os.path.join(self.round_dir, self.exe_name)
        self.run_cmd = settings.language_settings['exe_cmd'].format(
            exe_path=self.exe_path
        ).split(' ')
        self.input_path = os.path.join(self.round_dir, 'in')
        self.output_path = os.path.join(self.round_dir, 'out')
        self.log_path = os.path.join(self.round_dir, 'run.log')

        self.seccomp_rule = settings.language_settings['seccomp_rule']
        self.max_time = settings.max_time
        self.max_real_time = self.max_time * 3
        self.max_memory = settings.max_memory * 1048576 if settings.lang != 'j' else -1

        self.run = dict(
            max_cpu_time=self.max_time,
            max_real_time=self.max_real_time,
            max_memory=self.max_memory,
            max_output_size=128 * 1024 * 1024,
            max_process_number=_judger.UNLIMITED,
            exe_path=self.run_cmd[0],
            input_path=self.input_path,
            output_path=self.output_path,
            error_path=self.log_path,
            args=self.run_cmd[1:],
            env=[("PATH=" + os.getenv("PATH"))] + settings.language_settings['env'],
            log_path=self.log_path,
            seccomp_rule_path=self.seccomp_rule,
            uid=0,  # not safe
            gid=0
        )