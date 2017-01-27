# Compare two word lists
# Start with length of list, and then words follow

from testlib.compare import *

if __name__ == '__main__':
    word_ncmp('stdin', sys.argv[2], 'stdout')
