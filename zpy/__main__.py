'''
Usage:
    zpy
    zpy (--help | --version)

'''

import sys
import docopt
import zpy


def main(args=None):
    try:
        args = args if args is not None else sys.argv[1:]
        args = docopt.docopt(__doc__, argv=args, version=zpy.__version__)
    except docopt.DocoptExit as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
