import shutil
from config import *
import uuid

try:
    # Making folders
    if os.path.exists(JUDGE_BASE_DIR):
        if not os.path.exists(JUDGE_BASE_DIR_PAST):
            os.mkdir(JUDGE_BASE_DIR_PAST)
        shutil.copytree(JUDGE_BASE_DIR, os.path.join(JUDGE_BASE_DIR_PAST, str(uuid.uuid1())))
        shutil.rmtree(JUDGE_BASE_DIR)
    os.mkdir(JUDGE_BASE_DIR)
    os.mkdir(SUBMISSION_DIR)
    os.mkdir(ROUND_DIR)
    os.mkdir(DATA_DIR)
    os.mkdir(PRETEST_DIR)
    os.mkdir(TMP_DIR)
    shutil.copytree(os.path.join(BASE_DIR, 'include'), INCLUDE_DIR)

    # Close debug mode
    with open('local_config.py', 'w') as f:
        f.write('DEBUG = False')

except FileNotFoundError as e:
    print(e)
    print('Are you sure this copy is complete?')
except PermissionError as e:
    print('Use root please.')
except OSError as e:
    print(e)
