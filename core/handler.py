import os
from random import Random
from .program import Program
from .judge import Judge
from .tester import Tester
from config import *
import re

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

        self.round_log = open(os.path.join(ROUND_DIR, 'round.log'), "w")


    def run(self):
        # TEST
        for submission in self.submissions:
            test_result = Tester(submission).test()
            if test_result['error'] != ERROR_CODE[PRETEST_PASSED]:
                return test_result
        test_result = Tester(self.judge).test()
        if test_result['error'] != ERROR_CODE[PRETEST_PASSED]:
            return test_result

        for file in os.listdir(DATA_DIR):
            if os.path.exists(self.ready_for_input):
                os.remove(self.ready_for_input)
            os.symlink(file, self.ready_for_input)

            self.round_log.write('####Based on input data %s:\n\n' % file)

            # Start Running

            r = Random()
            r.shuffle(self.submissions)
            cnt = 0

            while True:
                running_result = self.submissions[cnt].run()

                # Writing log
                log_info = dict(
                    time=running_result['cpu_time'],
                    memory=running_result['memory'],
                    exit_code=running_result['exit_code'],
                    score=0,
                    result=running_result['result']
                )
                to_continue = False
                self.round_log.write('#####Run #%d: time: %dms., memory: %dKB, exit code: %d, '
                                     'running result: %s, score: %d, \n\n')

                # Handle Errors
                if running_result['result'] == 0:
                    # Cope with Judge
                    self.judge.run()
                    judge_result = self._judge_text_processing()

                if not to_continue:
                    self.round_log.write('####Judge has called to an end.\n')
                    self.round_log.write('#####Program ')

                cnt = (cnt + 1) % len(self.submissions)


    # Returning a dict of all the things to do
    def _judge_text_processing(self):
        result = dict()

        result['continue'] = False
        result['score'] = 0
        result['message'] = 0

        with open(self.judge.output_path, "r") as f:
            raw_text = re.split(r'[^A-Za-z0-9]', f.read())
            text = []
            for t in raw_text:
                if t != '':
                    text.append(t)
            text = ' '.join(text)
            text = text.lower()

            if re.match(r'continue', text) is not None:
                result['continue'] = True

            if re.match(r'stop', text) is not None:
                result['continue'] = False

            if re.match(r'ok|yes|right|correct', text) is not None:
                result['score'] = 100
                result['message'] = CORRECT

            if re.match(r'no|wrong', text) is not None:
                result['score'] = 0
                result['message'] = WRONG_ANSWER

            M = re.match(r'score[ds]? \d+', text)
            if M is not None:
                num = int(re.match(r'\d+', M.group()).group())
                num = min(max(num, 0), 100)
                result['score'] = num
                result['message'] = OK

            if re.match(r'idleness limit exceeded', text) is not None:
                result['score'] = 0
                result['continue'] = False
                result['message'] = IDLENESS_LIMIT_EXCEEDED

        return result