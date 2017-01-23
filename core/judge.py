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
        self.judge_new_input_path = os.path.join(self.round_dir, 'judge_new_input')
        self.run_cmd.append(self.judge_in_path)
        self.run_cmd.append(self.judge_ans_path)
        self.run_cmd.append(self.judge_new_input_path)

    def run(self, in_link=None, ans_link=None):
        try:
            assert ans_link is not None
            if os.path.exists(self.judge_ans_path):
                os.remove(self.judge_ans_path)
            os.symlink(ans_link, self.judge_ans_path)
        except (AssertionError, FileNotFoundError, FileExistsError):
            open(self.judge_ans_path, "w+").close()

        try:
            assert in_link is not None
            if os.path.exists(self.judge_in_path):
                os.remove(self.judge_in_path)
            os.symlink(in_link, self.judge_in_path)
        except (AssertionError, FileNotFoundError, FileExistsError):
            open(self.judge_in_path, "w+").close()

        super().run()
