from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256

import zpy.util


def encrypt_stream_v1(identity, stdin, stdout):
    magic = b"zpy\x01"
    rng = Random.new()
    iv = rng.read(16)  # counter mode prefix
    key = rng.read(32)  # random AES-256 key
    # AES-256 in counter mode
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, "big"))
    aes = AES.new(key, mode=AES.MODE_CTR, counter=ctr)
    mac = HMAC.new(key, digestmod=SHA256)  # HMAC-SHA256 for ciphertext
    # the AES-256 key is encrypte with the users rsa private key
    key = PKCS1_OAEP.new(zpy.util.load_identity(identity)).encrypt(key)
    # the output stream begins with the 8 byte iv, the length of the
    # encrypted AES-256 key in two bytes and the encrypted key itself
    header = magic + iv + len(key).to_bytes(2, "big") + key
    stdout.write(header)
    # starting the hmac with the file header ensures the header cannot
    # be modified (e.g. to downgrade the verification protocol)
    mac.update(header)
    while True:
        # encrypt in chunks of 65535 bytes (a two byte integer)
        chunk = aes.encrypt(stdin.read(0xFFFF))
        if chunk:
            # write the length of the encrypted chunk and the chunk itself
            stdout.write(len(chunk).to_bytes(2, "big") + chunk)
            # update the hmac with the ciphertext
            mac.update(chunk)
        if len(chunk) < 0xFFFF:
            break
    # the two null bytes represent an empty chunk, i.e. the end of the
    # ciphertext, the last 32 bytes of the output stream are the
    # HMAC-SHA256 digest
    stdout.write(b"\x00\x00" + mac.digest())


def encrypt(identity, filename, version=1):
    with open(filename, "rb") as stdin:
        with open("/dev/stdout", "wb") as stdout:
            if version == 1:
                encrypt_stream_v1(identity, stdin, stdout)
            else:
                raise RuntimeError("invalid version number")
    return 0
