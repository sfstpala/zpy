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

import unittest
import unittest.mock
import io
import binascii
import contextlib
import Crypto.Hash
import zpy.encrypt


class EncryptTest(unittest.TestCase):

    @unittest.mock.patch("Crypto.Random.new")
    @unittest.mock.patch("zpy.util.load_identity")
    @unittest.mock.patch("Crypto.Cipher.AES.new")
    @unittest.mock.patch("Crypto.Cipher.PKCS1_OAEP.new")
    @unittest.mock.patch("Crypto.Util.Counter.new")
    @unittest.mock.patch("Crypto.Hash.HMAC.new")
    def test_encrypt_stream_v2(
            self, new_HMAC, new_Counter, new_PKCS1_OAEP, new_AES,
            load_identity, new_Random):
        load_identity.return_value = "..."
        stdin = io.BytesIO(b"\xEE" * 0xFFFF)
        stdout = io.BytesIO()
        iv = b"\x00" * 15 + b"\x01"
        key = b"\xFF" * 32 + b"\xDD" * 32
        new_Random.return_value = io.BytesIO(iv + key)
        new_PKCS1_OAEP.return_value.encrypt.return_value = b"\xAA"
        new_AES.return_value.encrypt.side_effect = lambda x: x
        new_HMAC.return_value.digest.return_value = b"\xCC"
        zpy.encrypt.encrypt_stream_v2("id", stdin, stdout)
        counter = new_Counter.return_value
        new_AES.assert_called_once_with(b"\xFF" * 32, mode=6, counter=counter)
        new_Counter.assert_called_once_with(
            128, initial_value=int.from_bytes(iv, "big"))
        new_HMAC.assert_called_once_with(
            b"\xDD" * 32, digestmod=Crypto.Hash.SHA256)
        load_identity.assert_called_once_with("id")
        res = binascii.hexlify(stdout.getvalue()).decode()
        self.assertEqual(res[:54], (
            "7a7079000002"  # magic
            "00000000000000000000000000000001"  # iv
            "0001"  # length of encrypted key
            "aa"  # encrypted key
            "ffff"  # length of the first chunk
        ))
        self.assertEqual(res[54:-6], (
            "ee"  # first encrypted chunk (65535 bytes)
        ) * 0xFFFF)
        self.assertEqual(res[-6:], (
            "0000"  # length of next (last) chunk
            "cc"  # mac
        ))

    @unittest.mock.patch("zpy.encrypt.encrypt_stream_v2")
    @unittest.mock.patch("zpy.util.EncodingWriter")
    def test_encrypt_stream_v2_base64(self, EncodingWriter, encrypt_stream_v2):
        writer = EncodingWriter.return_value.__enter__.return_value
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        zpy.encrypt.encrypt_stream_v2_base64("id", stdin, stdout)
        zpy.encrypt.encrypt_stream_v2.assert_called_once_with(
            "id", stdin, writer)
        EncodingWriter.assert_called_once_with(stdout)

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("zpy.encrypt.encrypt_stream_v2_base64")
    def test_encrypt(self, encrypt_stream_v2_base64, open):
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        open.side_effect = [
            contextlib.closing(stdin),
            contextlib.closing(stdout),
        ]
        zpy.encrypt.encrypt("id", "/dev/stdin")
        self.assertEqual(open.mock_calls, [
            unittest.mock.call("/dev/stdin", "rb"),
            unittest.mock.call("/dev/stdout", "wb"),
        ])
        encrypt_stream_v2_base64.assert_called_once_with("id", stdin, stdout)

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("zpy.encrypt.encrypt_stream_v2")
    def test_encrypt_raw(self, encrypt_stream_v2, open):
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        open.side_effect = [
            contextlib.closing(stdin),
            contextlib.closing(stdout),
        ]
        zpy.encrypt.encrypt("id", "/dev/stdin", raw=True)
        self.assertEqual(open.mock_calls, [
            unittest.mock.call("/dev/stdin", "rb"),
            unittest.mock.call("/dev/stdout", "wb"),
        ])
        encrypt_stream_v2.assert_called_once_with("id", stdin, stdout)

    @unittest.mock.patch("builtins.open")
    def test_encrypt_invalid_header(self, open):
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        open.side_effect = [
            contextlib.closing(stdin),
            contextlib.closing(stdout),
        ]
        with self.assertRaises(RuntimeError):
            zpy.encrypt.encrypt("id", "/dev/stdin", version=0)
        self.assertEqual(open.mock_calls, [
            unittest.mock.call("/dev/stdin", "rb"),
            unittest.mock.call("/dev/stdout", "wb"),
        ])
