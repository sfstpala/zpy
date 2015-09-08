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

import base64
import subprocess

from Crypto.PublicKey import RSA


def openssl(*args):
    return subprocess.check_output(["openssl"] + list(args))


def load_identity(filename):
    try:
        with open(filename) as f:
            return RSA.importKey(f.read())
    except ValueError:
        pass
    output = openssl("rsa", "-in", filename)
    return RSA.importKey(output)


class EncodingWriter:

    def __init__(self, fp):
        self.fp = fp
        self.bf = b""

    def write(self, data):
        self.bf += data
        while len(self.bf) >= 48:
            data, self.bf = self.bf[:48], self.bf[48:]
            self.fp.write(base64.b64encode(data) + b"\n")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.bf:
            self.fp.write(base64.b64encode(self.bf))
            self.fp.write(b"\n")


class DecodingReader:

    def __init__(self, fp):
        self.fp = fp
        self.bf = b""

    def write(self, data):
        self.bf += data

    def read(self, n):
        data = self.bf[:n]
        self.bf = self.bf[len(data):]
        return data

    def __enter__(self):
        base64.decode(self.fp, self)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
