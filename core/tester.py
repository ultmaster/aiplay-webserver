import shutil, uuid
from .program import Program
from .judge import Judge
from config import *
from .utils import *


# Tester: to test whether a submission is a valid submission
class Tester(object):

    def __init__(self, arg_program, judge=None):
        if isinstance(arg_program, Program):
            # Come from handler
            self.program = arg_program
            self.judge = judge
        else:
            # Come from outside
            self.program = Program(arg_program['submission'], arg_program['config'])
            self.judge = Judge(arg_program['judge'], arg_program['config'])
        self.error = PRETEST_PASSED
        self.message = 'none'

        self.pretest_dir = os.path.join(PRETEST_DIR, str(self.program.problem_id))
        self.round_dir = os.path.join(ROUND_DIR, str(uuid.uuid1()))
        os.mkdir(self.round_dir)
        self.input_path = os.path.join(self.round_dir, 'in')
        self.ans_path = os.path.join(self.round_dir, 'judge_ans')

    def test(self):
        if self.test_compile() and self.judge is not None:
            self.test_run()
        self.message = 'Submission #%d:\n' % self.program.submission_id + self.message
        return {'code': self.error, 'message': self.message}

    def test_compile(self):
        if not self.program.compile():
            self.error = COMPILE_ERROR
            self.message = read_partial_data_from_file(self.program.compile_out_path, 1024)
            if self.message == '':
                self.message = read_partial_data_from_file(self.program.compile_log_path, 1024)
            return False
        return True

    def test_run(self):

        # IMPORT DATA
        data_list = import_data(self.pretest_dir)
        sum_score = 0

        for data in data_list:
            input_file = data[0]
            ans_file = data[1]

            if os.path.exists(self.input_path):
                os.remove(self.input_path)
            shutil.copyfile(os.path.join(self.pretest_dir, input_file), self.input_path)

            if os.path.exists(self.ans_path):
                os.remove(self.ans_path)
            if ans_file is not None:
                shutil.copyfile(os.path.join(self.pretest_dir, ans_file), self.ans_path)

            running_result = self.program.run()
            judge_result = self.judge.run(pretest=True)
            sum_score += judge_result['score']

            if running_result['result'] > 0:  # fatal error
                self.error = PRETEST_FAILED

        if len(data_list) > 0 and sum_score == 0:
            self.error = PRETEST_FAILED

        print(('Pretest', self.program.submission_id, sum_score))

        # CLEAN UP
        for file in os.listdir(self.round_dir):
            os.remove(os.path.join(self.round_dir, file))

        return False if self.error == PRETEST_FAILED else True
