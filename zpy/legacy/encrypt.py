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

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256

import zpy.util


def encrypt_stream_v1_base64(identity, stdin, stdout):
    with zpy.util.EncodingWriter(stdout) as stdout:
        return encrypt_stream_v1(identity, stdin, stdout)


def encrypt_stream_v1(identity, stdin, stdout):
    magic = b"zpy\x00\x00\x01"
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
