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
