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
        self.input_path = os.path.join(self.round_dir, 'in')
        self.output_path = os.path.join(self.round_dir, 'out')
        self.ans_path = os.path.join(self.round_dir, 'judge_ans')
        self.round_log_path = os.path.join(self.round_dir, 'round.log')

        self.round_log = open(self.round_log_path, "w")
        self.dumped = False

    def run(self):
        if self.dumped:
            # WHAT THE HELL?
            return { 'code': SYSTEM_ERROR }
        self.dumped = True
        # TEST
        for submission in self.submissions:
            test_result = Tester(submission).test()
            if test_result['code'] != PRETEST_PASSED:
                return test_result
        test_result = Tester(self.judge).test()
        if test_result['code'] != PRETEST_PASSED:
            return test_result

        # IMPORT DATA
        data_list = import_data(self.data_dir)

        # INIT
        for i in range(len(self.submissions)):
            self.submissions[i].sum_score = 0

        for data in data_list:
            input_file = data[0]
            ans_file = data[1]
            weight = data[2]

            # use copy instead of link to prevent chmod problems
            if os.path.exists(self.input_path):
                os.remove(self.input_path)
            shutil.copyfile(os.path.join(self.data_dir, input_file), self.input_path)

            if os.path.exists(self.ans_path):
                os.remove(self.ans_path)
            if ans_file is not None:
                shutil.copyfile(os.path.join(self.data_dir, ans_file), self.ans_path)

            self.round_log.write('#### Based on input data %s, data weight %d:\n\n' % (input_file, weight))

            # Start Running

            r = Random()
            r.shuffle(self.submissions)
            for i in range(len(self.submissions)):
                self.submissions[i].score = 0
                self.submissions[i].sum_time = 0
                self.submissions[i].sum_memory = 0
            cnt = 1
            run_count = 1

            while True:
                running_result = self.submissions[cnt].run()

                # Save data
                log_info = dict(
                    cnt=run_count,
                    program=self.submissions[cnt].submission_id,
                    time=running_result['cpu_time'],
                    memory=running_result['memory'] // 1024,
                    exit_code=running_result['exit_code'],
                    score=0,
                    result=running_result['result']
                )
                in_data = read_partial_data_from_file(self.input_path, 1024)
                out_data = read_partial_data_from_file(self.output_path, 1024)
                judge_data = 'none'

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
                    if os.path.exists(self.input_path):
                        os.remove(self.input_path)
                    shutil.copyfile(self.judge.judge_new_input_path, self.input_path)

                elif running_result['result'] == RUNTIME_ERROR:
                    out_data = read_partial_data_from_file(self.judge.log_path, 1024)

                # Write Log
                log_info['result'] = ERROR_CODE[log_info['result']]
                self.round_log.write('##### Run #{cnt} (submission #{program})\n'
                                     '**time: {time}ms., memory: {memory}KB, '
                                     'exit code: {exit_code}, verdict: {result}, raw score: {score}.**\n'
                                     .format(**log_info))
                # DEBUG
                # print('Run #{cnt}: submission: #{program}, time: {time}ms., memory: {memory}KB, '
                #       'exit code: {exit_code}, running result: {result}, score: {score}. '
                #       .format(**log_info))
                self.round_log.write('input:\n```%s```\n' % format_code_for_markdown(in_data))
                self.round_log.write('output:\n```%s```\n' % format_code_for_markdown(out_data))
                self.round_log.write('judge:\n```%s```\n' % format_code_for_markdown(judge_data))

                # Deal with the game
                self.submissions[cnt].score += log_info['score']
                if not _continue:
                    break

                cnt = (cnt + 1) % len(self.submissions)
                run_count += 1

            # Round complete
            if run_count > 1:
                self.round_log.write('##### Judge has called an end to this round.\n')
                for submission in self.submissions:
                    self.round_log.write('#%d time: %dms., memory: %dKB, score: %d.\n\n' % (
                        submission.submission_id, submission.sum_time, submission.sum_memory, submission.score))
            for i in range(len(self.submissions)):
                self.submissions[i].sum_score += int(self.submissions[i].score / 100 * weight)

        # CLEAN UP
        json_result = dict()
        json_result['code'] = FINISHED
        json_result['score'] = dict()

        self.round_log.write('##### Conclusion:\n')
        for submission in self.submissions:
            self.round_log.write('#%d has a total score of %d.\n\n' % (submission.submission_id, submission.sum_score))
            json_result['score'][submission.submission_id] = submission.sum_score
        for file in os.listdir(self.round_dir):
            if file != 'round.log':
                os.remove(os.path.join(self.round_dir, file))

        self.round_log.close()
        json_result['message'] = open(self.round_log_path, "r").read()
        return json_result

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

            if re.search(r'continue', text) is not None:
                result['continue'] = True

            if re.search(r'stop', text) is not None:
                result['continue'] = False

            if re.search(r'ok|yes|right|correct', text) is not None:
                result['score'] = 100
                result['message'] = CORRECT

            if re.search(r'no|wrong', text) is not None:
                result['score'] = 0
                result['message'] = WRONG_ANSWER

            pattern = re.search(r'score[ds]? \d+', text)
            if pattern is not None:
                num = int(re.search(r'\d+', pattern.group()).group())
                num = min(max(num, 0), 100)
                result['score'] = num
                result['message'] = OK

            if re.search(r'idleness limit exceeded', text) is not None:
                result['score'] = 0
                result['continue'] = False
                result['message'] = IDLENESS_LIMIT_EXCEEDED

        return result
