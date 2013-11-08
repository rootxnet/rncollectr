"""Random number plugin.

Usage:
    random.py [options]

Options:
    --min-number N   Lower limit for random number generator [default: 0]
    --max-number N   Higher limit for random number generator [default: 100]
"""

from random import randrange
from docopt import docopt

if __name__ == "__main__":
    arg = docopt(__doc__, version="Random number plugin 1.0")
    print(randrange(int(arg["--min-number"]), int(arg["--max-number"])))