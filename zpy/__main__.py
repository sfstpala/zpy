# Copyright (C) 2015  Stefano Palazzo <stefano.palazzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
zpy - quickly encrypt files with your ssh identity.

Usage:
    zpy [options] encrypt [<filename>] [-r]
    zpy [options] decrypt [<filename>]
    zpy (--help | --copying | --version)

Options:
    -i <identity>, --identity=<identity>
        ssh private or public key file [default: ~/.ssh/id_rsa]

Encryption options:
    -r, --raw   skip base64 encoding

Examples:
    zpy encrypt passwords.txt
    zpy encrypt passwords.txt --raw > encrypted.bin
    zpy encrypt -i id_rsa.pub message.txt > message.zpy
    zpy decrypt encrypted.bin > passwords.txt

Copyright notice:
    Copyright (C) 2015  Stefano Palazzo <stefano.palazzo@gmail.com>
    This program comes with ABSOLUTELY NO WARRANTY;
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `zpy --copying` for details.
"""

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
    if args.get("--copying"):
        print(zpy.__copying__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
