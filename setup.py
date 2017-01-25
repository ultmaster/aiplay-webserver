import os, sys

try:
    sys.path.count('/judge_server/include')
    os.mkdir('/aipWebserver')
    os.mkdir('/aipWebserver/submission')
    os.mkdir('/aipWebserver/round')
    os.mkdir('/aipWebserver/data')
    os.mkdir('/aipWebserver/compile')
    os.mkdir('/aipWebserver/data/1001')
except FileExistsError:
    print('Folder already exists.')
except PermissionError:
    print('Use root please.')