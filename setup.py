import os

try:
    os.mkdir('/aipWebserver')
    os.mkdir('/aipWebserver/submission')
    os.mkdir('/aipWebserver/round')
    os.mkdir('/aipWebserver/data')
    os.mkdir('/aipWebserver/compile')
except FileExistsError:
    print('Folder already exists.')
except PermissionError:
    print('Use root please.')