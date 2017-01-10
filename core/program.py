from languages import _LANGUAGE_SETTINGS
from config import COMPILE_DIR, SUBMISSION_DIR, DEBUG
import _judger
import os
from .settings import BaseSettings, CompileSettings, RunSettings


class Program(object):
    def __init__(self, submission_config, round_config):
        self.settings = BaseSettings(submission_config, round_config)
        self.compile_settings = CompileSettings(self.settings)
        self.run_settings = RunSettings(self.settings)

    def _compile(self):
        os.mkdir(self.compile_settings.submission_dir)
        with open(self.compile_settings.src_path, 'w') as f:
            f.write(self.settings.code)
        print(self.compile_settings.compile)
        return _judger.run(**self.compile_settings.compile)

    def _run(self):
        pass


class Submission(Program):
    def __init__(self, submission_config, round_config):
        super(Submission, self).__init__(submission_config, round_config)

    def compile(self):
        # TODO if compile result exist
        result = self._compile()
        print(":::" + self.settings.lang)
        print(result)
        if result["result"] != _judger.RESULT_SUCCESS:
            if not os.path.exists(self.compile_settings.compile_out_path):
                with open(self.compile_settings.compile_out_path, 'w') as f:
                    f.write("Error Code=" + result['error'])
            return False
        else:
            return True
