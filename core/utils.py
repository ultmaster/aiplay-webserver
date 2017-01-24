import re

def import_data(path, pattern=None):
    pass


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
