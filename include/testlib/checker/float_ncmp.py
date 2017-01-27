# Compare two real number lists, maximum absolute error is predefined in EPS
# Start with length of list, and then real numbers follow

from testlib.compare import *

EPS = 1e-6

if __name__ == '__main__':
    float_ncmp('stdin', sys.argv[2], 'stdout', EPS)
