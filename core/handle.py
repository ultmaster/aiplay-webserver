import os
from config import SUBMISSION_DIR
from .compiler import _compile
from languages import LANGUAGE_SETTINGS
import _judger


class Handler(object):
    def __init__(self, data):
        for k, v in data:
            setattr(self, k, v)

    def run(self):
        if self.compile():
            # running!
            pass
        else:
            return "RE"

    def compile(self):
        for submission in self.submissions:
            if not self._compile_one(submission):
                return False
        return True

    @staticmethod
    def _compile_one(submission):
        submission_dir = os.path.join(SUBMISSION_DIR, str(submission['id']))
        if os.path.exists(submission_dir):
            return True
        else:
            language_setting = LANGUAGE_SETTINGS[submission['language']]
            os.mkdir(submission_dir)
            src_path = os.path.join(submission_dir, language_setting['src_name'])
            return _compile(language_setting, src_path, str(submission['id']))
