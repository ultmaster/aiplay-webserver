import os
import re
import shutil
from random import Random
from .program import Program
from .judge import Judge
from .tester import Tester
from .utils import *
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
        self.ready_for_output = os.path.join(self.round_dir, 'out')

        self.round_log = open(os.path.join(self.round_dir, 'round.log'), "w")

    def run(self):
        # TEST
        for submission in self.submissions:
            test_result = Tester(submission).test()
            if test_result['error'] != ERROR_CODE[PRETEST_PASSED]:
                return test_result
        test_result = Tester(self.judge).test()
        if test_result['error'] != ERROR_CODE[PRETEST_PASSED]:
            return test_result

        for file in os.listdir(self.data_dir):
            if os.path.exists(self.ready_for_input):
                os.remove(self.ready_for_input)
            os.symlink(os.path.join(self.data_dir, file), self.ready_for_input)
            with open(os.path.join(self.data_dir, file), "r") as f:
                print(f.read())

            # TODO: weight
            weight = 0

            self.round_log.write('####Based on input data %s, data weight %d:\n\n' % (file, weight))

            # Start Running

            r = Random()
            r.shuffle(self.submissions)
            cnt = 1

            while True:
                running_result = self.submissions[cnt].run()

                # Save rundata
                log_info = dict(
                    cnt=cnt,
                    program=self.submissions[cnt].submission_id,
                    time=running_result['cpu_time'],
                    memory=running_result['memory'] // 1024,
                    exit_code=running_result['exit_code'],
                    score=0,
                    result=running_result['result']
                )
                in_data = read_partial_data_from_file(self.ready_for_input, 1024)
                out_data = read_partial_data_from_file(self.ready_for_output, 1024)
                judge_data = ''

                _continue = False

                # Handle Errors
                if running_result['result'] == 0:
                    # Cope with Judge
                    self.judge.run()
                    judge_result = self._judge_text_processing()
                    _continue = judge_result['continue']
                    log_info['score'] = judge_result['score']
                    log_info['result'] = judge_result['message']
                    judge_data = judge_result['data']

                    # New input
                    if os.path.exists(self.ready_for_input):
                        os.remove(self.ready_for_input)
                    shutil.copyfile(self.judge.judge_new_input_path, self.ready_for_input)

                # Write Log
                log_info['result'] = ERROR_CODE[log_info['result']]
                self.round_log.write('#####Run #{cnt}: submission: #{program}, time: {time}ms., memory: {memory}KB, '
                                     'exit code: {exit_code}, running result: {result}, score: {score}. \n\n'
                                     .format(**log_info))
                # DEBUG
                print('Run #{cnt}: submission: #{program}, time: {time}ms., memory: {memory}KB, '
                      'exit code: {exit_code}, running result: {result}, score: {score}. \n\n'
                      .format(**log_info))
                self.round_log.write('**input:**\n```%s```\n' % in_data)
                self.round_log.write('**output:**\n```%s```\n' % out_data)
                self.round_log.write('**judge:**\n```%s```\n\n' % judge_data)

                # Deal with the game
                self.submissions[cnt].score += log_info['score']
                if not _continue:
                    # GAME OVER
                    if cnt > 1:
                        self.round_log.write('####Judge has called to an end for this round.\n')
                        for submission in self.submissions:
                            self.round_log.write('#%d scored %d. '.format(submission.submission_id, submission.score))
                        self.round_log.write('\n\n')
                    break

                cnt = (cnt + 1) % len(self.submissions)

    # Returning a dict of all the things to do
    def _judge_text_processing(self):
        result = dict()

        result['continue'] = False
        result['score'] = 0
        result['message'] = 0
        result['data'] = ''

        with open(self.judge.output_path, "r") as f:
            result['data'] = f.read()
            raw_text = re.split(r'[^A-Za-z0-9]', result['data'])
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

            pattern = re.match(r'score[ds]? \d+', text)
            if pattern is not None:
                num = int(re.match(r'\d+', pattern.group()).group())
                num = min(max(num, 0), 100)
                result['score'] = num
                result['message'] = OK

            if re.match(r'idleness limit exceeded', text) is not None:
                result['score'] = 0
                result['continue'] = False
                result['message'] = IDLENESS_LIMIT_EXCEEDED

        print(result)
        return result
