import os
from .program import Submission
import shutil
from config import DATA_DIR, ROUND_DIR

class Handler(object):
    def __init__(self, data):
        submission_list = data['submissions']
        round_config = data['round_config']
        self.problem_id = round_config['problem_id']
        self.round_id = round_config['round_id']
        self.data_dir = os.path.join(DATA_DIR, str(self.problem_id))
        self.round_dir = os.path.join(ROUND_DIR, str(self.round_id))

        self.submissions = []
        for submission in submission_list:
            self.submissions.append(Submission(submission, round_config))
        self.judge = Submission(data['judge'], round_config)

    def run(self):
        if not self.compile():
            raise BaseException("Some accident just happened.")
        # TODO: redirect input

        for submission in self.submissions:
            submission.run()
        self.judge.run()

    def compile(self):
        for submission in self.submissions:
            if not submission.compile():
                return False
        if not self.judge.compile():
            return False
        return True

