# Compare two real numbers, maximum absolute error is predefined in EPS
# One real number in file exactly, then it must be EOF

from testlib.compare import *

EPS = 1e-6

if __name__ == '__main__':
    float_ocmp('stdin', sys.argv[2], 'stdout', EPS)
