# Compare two files, filtering out spaces at end-of-line and blank lines at end-of-file

from testlib.compare import *

if __name__ == '__main__':
    file_cmp('stdin', sys.argv[2], 'stdout')
