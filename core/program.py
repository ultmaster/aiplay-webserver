from languages import _LANGUAGE_SETTINGS
from config import COMPILE_DIR, SUBMISSION_DIR, DEBUG
import _judger
import os
from .settings import BaseSettings, CompileSettings, RunSettings
import shutil


class Program(object):
    def __init__(self, submission_config, round_config):
        self.settings = BaseSettings(submission_config, round_config)
        self.compile_settings = CompileSettings(self.settings)
        self.run_settings = RunSettings(self.settings)

    def _compile(self):
        return _judger.run(**self.compile_settings.compile)

    def _run(self):
        print(self.run_settings.run)
        return _judger.run(**self.run_settings.run)


class Submission(Program):
    def __init__(self, submission_config, round_config):
        super(Submission, self).__init__(submission_config, round_config)

    def compile(self):
        # TODO if compile result exist
        with open(self.compile_settings.src_path, 'w') as f:
            f.write(self.settings.code)
        result = self._compile()
        print("Compile Result of " + self.settings.lang + ": " + str(result))
        if result["result"] != _judger.RESULT_SUCCESS:
            if not os.path.exists(self.compile_settings.compile_out_path):
                with open(self.compile_settings.compile_out_path, 'w') as f:
                    f.write("Error Code=" + result['error'])
            return False
        else:
            return True

    def run(self, input='', output=''):
        if input != '':
            self.run_settings.update_input_path(input)
        if output != '':
            self.run_settings.update_output_path(output)
        # TEST
        with open(self.run_settings.input_path, 'w') as f:
            f.write('hahaha')

        result = self._run()
        print("Running Result of " + self.settings.lang + ": " + str(result))
        if result["result"] != _judger.RESULT_SUCCESS:
            return False
        return True