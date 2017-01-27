# Compare two sequences of real numbers, maximum absolute error is predefined in EPS
# Keep doing that until End Of File

from testlib.compare import *

EPS = 1e-6

if __name__ == '__main__':
    float_cmp('stdin', sys.argv[2], 'stdout', EPS)
