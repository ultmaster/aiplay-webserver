import os
from config import SUBMISSION_DIR
from .compiler import _compile
from languages import LANGUAGE_SETTINGS
import _judger


class Handler(object):
    def __init__(self, data):
        for k, v in data.items():
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
        language_setting = LANGUAGE_SETTINGS[submission['language']]
        src_path = os.path.join(SUBMISSION_DIR, str(submission['id'])+language_setting['src_name'])
        if os.path.exists(src_path):
            return True
        else:
            with open(src_path, 'w') as f:
                f.write(submission['code'])
            return _compile(language_setting, src_path, str(submission['id']))
