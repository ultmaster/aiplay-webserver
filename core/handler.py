import os
from .program import Program
import shutil
from config import DATA_DIR, ROUND_DIR

class Handler(object):
    def __init__(self, data):
        submission_list = data['submissions']
        round_config = data['config']
        self.problem_id = round_config['problem_id']
        self.round_id = round_config['round_id']
        self.data_dir = os.path.join(DATA_DIR, str(self.problem_id))
        self.round_dir = os.path.join(ROUND_DIR, str(self.round_id))

        self.submissions = []
        for submission in submission_list:
            self.submissions.append(Program(submission, round_config))
        self.judge = Program(data['judge'], round_config)

    def control(self):
        for f in os.listdir(DATA_DIR):
            # List all input data
            os.symlink(f, os.path.join(DATA_DIR, 'in'))


    def run(self):
        if not self.compile():
            raise BaseException("Some accident just happened.")

        for submission in self.submissions:
            result = submission.run()
            #if result["result"] != _judger.RESULT_SUCCESS:
            #    return
        self.judge.run()

    def compile(self):
        for submission in self.submissions:
            if not submission.compile():
                return False
        if not self.judge.compile():
            return False
        return True

