from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256

import zpy.util


def decrypt_stream_v1_base64(identity, stdin, stdout):
    with zpy.util.DecodingReader(stdin) as stdin:
        return decrypt_stream_v1(identity, stdin, stdout)


def decrypt_stream_v1(identity, stdin, stdout):
    magic = b"zpy\x00\x00\x01"  # this has already been read from stdin
    # the first 8 bytes of the input stream are the aes counter iv
    iv = stdin.read(16)
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, "big"))
    key_size = stdin.read(2)
    key = stdin.read(int.from_bytes(key_size, "big"))
    header = magic + iv + key_size + key
    # read the encrypted symmetric key and decrypt it with
    # the rsa private key (the length depends on the key size)
    key = PKCS1_OAEP.new(zpy.util.load_identity(identity)).decrypt(key)
    # aes in counter mode and encrypt-then-mac
    aes = AES.new(key, mode=AES.MODE_CTR, counter=ctr)
    mac = HMAC.new(key, digestmod=SHA256)
    mac.update(header)
    while True:
        # each variable length chunk begins with its length in 2 bytes
        # which limits the length to 0xffff (65535) bytes
        chunk = stdin.read(int.from_bytes(stdin.read(2), "big"))
        # update the hmac before decrypting
        mac.update(chunk)
        stdout.write(aes.decrypt(chunk))
        if not chunk:
            break
    # the last 32 bytes of the message are the ciphertext hmac
    if mac.digest() != stdin.read(32):
        raise RuntimeError("hmac error")


def decrypt(identity, filename):
    with open(filename, "rb") as stdin:
        with open("/dev/stdout", "wb") as stdout:
            header = stdin.read(4)
            if header == b"enB5":
                header += stdin.read(4)
            else:
                header += stdin.read(2)
            if header == b"enB5AAAB":
                decrypt_stream_v1_base64(identity, stdin, stdout)
            elif header == b"zpy\x00\x00\x01":
                decrypt_stream_v1(identity, stdin, stdout)
            else:
                raise RuntimeError("invalid file header")
    return 0
