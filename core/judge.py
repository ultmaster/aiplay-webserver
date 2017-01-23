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
        self.judge_in_path = os.path.join(self.round_dir, 'in')
        self.judge_new_input_path = os.path.join(self.round_dir, 'judge_new_input')
        self.seccomp_rule_name = None
        self.base_run_cmd = self.run_cmd

    def generate_default_run_cmd(self):
        self.run_cmd = self.base_run_cmd
        self.run_cmd.append(self.judge_in_path)
        self.run_cmd.append(self.judge_ans_path)
        self.run_cmd.append(self.judge_new_input_path)

    def run(self, in_link=None, ans_link=None):
        self.generate_default_run_cmd()
        if in_link is not None:
            self.run_cmd[-3] = in_link
        if ans_link is not None:
            self.run_cmd[-2] = ans_link
        super().run()
