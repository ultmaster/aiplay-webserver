# Compare two words
# One word in file exactly, then it must be EOF

from testlib.compare import *

if __name__ == '__main__':
    word_ocmp('stdin', sys.argv[2], 'stdout')
