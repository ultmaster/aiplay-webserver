import os
from random import Random
from .program import Program
from .judge import Judge
from .tester import Tester
from config import *

class Handler(object):
    def __init__(self, data):
        submission_list = data['submissions']
        config = data['config']
        self.problem_id = config['problem_id']
        self.round_id = config['round_id']
        self.data_dir = os.path.join(DATA_DIR, str(self.problem_id))
        self.round_dir = os.path.join(ROUND_DIR, str(self.round_id))

        self.submissions = []
        for submission in submission_list:
            self.submissions.append(Program(submission, config))
        self.judge = Judge(data['judge'], config)
        self.ready_for_input = os.path.join(self.round_dir, 'in')

    def control(self):
        for file in os.listdir(DATA_DIR):
            if os.path.exists(self.ready_for_input):
                os.remove(self.ready_for_input)
            os.symlink(file, self.ready_for_input)



    def run(self):
        # TEST
        for submission in self.submissions:
            test_result = Tester(submission).test()
            if test_result['error'] != 0:
                return test_result
        test_result = Tester(self.judge).test()
        if test_result['error'] != 0:
            return test_result

        # Start Running
        r = Random()
        r.shuffle(self.submissions)
        cnt = 0
        while True:
            running_result = self.submissions[cnt].run()
            # Handle TLE
            if self.submissions[cnt].max_sum_time < 0:
                running_result['error'] = 1

            # Cope with Judge
            self.judge.run()

            cnt = (cnt + 1) % len(self.submissions)




