'''
zpy - quickly encrypt files with your ssh identity

Usage:
    zpy [options] encrypt [<filename>] [-r]
    zpy [options] decrypt [<filename>]
    zpy (--help | --version)

Options:
    -i <identity>, --identity=<identity>
        ssh private key file [default: ~/.ssh/id_rsa]

Encryption options:
    -r, --raw   skip base64 encoding

Examples:
    zpy encrypt passwords.txt
    zpy encrypt passwords.txt --raw > encrypted.bin
    zpy decrypt encrypted.bin > passwords.txt

'''

import sys
import os
import docopt
import zpy
import zpy.encrypt
import zpy.decrypt


def main(args=None):
    try:
        args = args if args is not None else sys.argv[1:]
        args = docopt.docopt(__doc__, argv=args, version=zpy.__version__)
    except docopt.DocoptExit as e:
        print(str(e), file=sys.stderr)
        return 2
    if args.get("encrypt"):
        return zpy.encrypt.encrypt(
            os.path.expanduser(args["--identity"]),
            os.path.expanduser(args["<filename>"] or "/dev/stdin"),
            raw=args["--raw"])
    if args.get("decrypt"):
        return zpy.decrypt.decrypt(
            os.path.expanduser(args["--identity"]),
            os.path.expanduser(args["<filename>"] or "/dev/stdin"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
