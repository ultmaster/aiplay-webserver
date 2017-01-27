# Compare two integers
# One integer in file exactly, then it must be EOF

from testlib.compare import *

if __name__ == '__main__':
    int_ocmp('stdin', sys.argv[2], 'stdout')
