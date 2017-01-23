import os
from .program import Program


# This class is meant to deal with IO for judges
# No further explanations...
class Judge(Program):
    def __init__(self, submission, config):
        super().__init__(submission, config)
        self.input_path = self.output_path
        self.output_path = os.path.join(self.round_dir, 'judge_result')
        self.ans_path = os.path.join(self.round_dir, 'ans')

    def run(self, ans_link=None):
        if ans_link is not None:
            os.symlink(ans_link, self.ans_path)
        super().run()
