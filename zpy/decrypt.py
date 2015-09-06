from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256


def decrypt_stream_v1(identity, stdin, stdout):
    # the first 8 bytes of the input stream are the aes counter iv
    ctr = Counter.new(64, stdin.read(8))
    with open(identity) as f:
        # read the encrypted symmetric key and decrypt it with
        # the rsa private key (the length depends on the key size)
        key = PKCS1_OAEP.new(RSA.importKey(f.read())).decrypt(
            stdin.read(int.from_bytes(stdin.read(2), "big")))
    # aes in counter mode and encrypt-then-mac
    aes = AES.new(key, mode=AES.MODE_CTR, counter=ctr)
    mac = HMAC.new(key, digestmod=SHA256)
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
            if stdin.read(4) == b"zpy\x01":
                decrypt_stream_v1(identity, stdin, stdout)
            else:
                raise RuntimeError("invalid file header")
    return 0
