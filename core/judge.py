import os
from .program import Program


# This class is meant to deal with IO for judges
# No further explanations...
class Judge(Program):
    def __init__(self, submission, config):
        super().__init__(submission, config)
        self.input_path = self.output_path
        self.output_path = os.path.join(self.round_dir, 'judge_result')
        self.judge_ans_path = os.path.join(self.round_dir, 'judge_ans')
        self.judge_in_path = os.path.join(self.round_dir, 'judge_in')

    def run(self, in_link=None, ans_link=None):
        if ans_link is not None:
            os.symlink(ans_link, self.judge_ans_path)
        if in_link is not None:
            os.symlink(in_link, self.judge_in_path)
        super().run()
