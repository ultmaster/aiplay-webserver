from .stream import *


def registerJudge(arg1, arg2, arg3, arg4, arg5):
    # 1. Original Input
    # 2. Original Output
    # 3. Original Answer
    # 4. New Input
    # 5. Judge Result

    in_file = InputStream(arg1)
    out_file = InputStream(arg2)
    ans_file = InputStream(arg3)
    new_file = OutputStream(arg4)
    result_file = OutputStream(arg5)
    return (in_file, out_file, ans_file, new_file, result_file)
