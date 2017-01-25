import re
import os
import json
import uuid


# Return a list of tuples containing inputs and corresponding outputs and weights
def import_data(path):

    def _find_a_integer_in_a_string(string):
        pat = re.search(r'\d+', string)
        return -1 if pat is None else int(pat.group())

    def _my_sort(lst):
        res = sorted(lst, key=lambda x: _find_a_integer_in_a_string(x[0]))
        return sorted(res, key=lambda x: re.sub(r'\d+', '', x[0]))

    def _search_a_list_for_string_ignore_case(lst, stg):
        for it in range(len(lst)):
            if stg.lower() == lst[it][0].lower():
                return it
        return -1
    try:
        with open(os.path.join(path, 'data.conf'), 'r') as f:
            config = json.loads(f.read())
    except (TypeError, FileNotFoundError):
        config = dict()

    raw_file_list = os.listdir(path)
    file_list = [(x, False) for x in raw_file_list]
    result = []
    patterns = {r'.in$': ['.out', '.ans'], r'input': ['output', 'answer']}

    for (in_pattern, out_pattern) in patterns.items():
        for i in range(len(file_list)):
            if file_list[i][1]:
                continue
            if re.search(in_pattern, file_list[i][0], re.IGNORECASE) is not None:
                for pattern in out_pattern:
                    try_str = re.sub(in_pattern, pattern, file_list[i][0], re.IGNORECASE)
                    find_result = _search_a_list_for_string_ignore_case(file_list, try_str)
                    if find_result >= 0:
                        file_list[i] = (file_list[i][0], True)
                        file_list[find_result] = (file_list[find_result][0], True)
                        result.append((file_list[i][0], file_list[find_result][0], config.get(file_list[i][0], 10)))
                        break
                if not file_list[i][1]:
                    file_list[i] = (file_list[i][0], True)
                    result.append((file_list[i][0], None, config.get(file_list[i][0], 10)))

    result = _my_sort(result)
    return result


def read_partial_data_from_file(filename, length):
    with open(filename, "r") as f:
        result = f.read(length)
    if len(result) >= length - 1:
        result += '\n......'
    return result


def format_code_for_markdown(code):
    code_length = len(code)
    if code_length > 0:
        start, end = 0, code_length - 1
        while start < code_length and code[start] == '\n':
            start += 1
        while end >= 0 and code[end] == '\n':
            end -= 1
        if end < start:
            return '\n\n'
        else:
            return '\n' + code[start:(end+1)] + '\n'
    return '\n\n'


def randomize_round_id():
    return str(uuid.uuid1())
