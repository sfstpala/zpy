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
import zpy.decrypt
import zpy.legacy.decrypt


class DecryptTest(unittest.TestCase):

    @unittest.mock.patch("zpy.util.load_identity")
    @unittest.mock.patch("Crypto.Cipher.AES.new")
    @unittest.mock.patch("Crypto.Cipher.PKCS1_OAEP.new")
    @unittest.mock.patch("Crypto.Util.Counter.new")
    @unittest.mock.patch("Crypto.Hash.HMAC.new")
    def test_decrypt_stream_v1(
            self, new_HMAC, new_Counter, new_PKCS1_OAEP, new_AES,
            load_identity):
        load_identity.return_value = "..."
        stdout = io.BytesIO()
        stdin = io.BytesIO(binascii.unhexlify((
            "00000000000000000000000000000001"  # iv
            "0001"  # length of encrypted key
            "aa"  # encrypted key
            "ffff"  # length of the first chunk
        ) + (
            "ee"
        ) * 0xFFFF + (
            "0000"
            "cc"
        )))
        key = b"\xFF" * 32
        iv = b"\x00" * 15 + b"\x01"
        new_PKCS1_OAEP.return_value.decrypt.return_value = b"\xFF" * 32
        new_AES.return_value.decrypt.side_effect = lambda x: x
        new_HMAC.return_value.digest.return_value = b"\xCC"
        zpy.legacy.decrypt.decrypt_stream_v1("id", stdin, stdout)
        self.assertEqual(stdout.getvalue(), b"\xEE" * 0xFFFF)
        load_identity.assert_called_once_with("id")
        counter = new_Counter.return_value
        new_Counter.assert_called_once_with(
            128, initial_value=int.from_bytes(iv, "big"))
        new_AES.assert_called_once_with(key, mode=6, counter=counter)
        stdin = io.BytesIO(binascii.unhexlify((
            "00000000000000000000000000000001"  # iv
            "0001"  # length of encrypted key
            "aa"  # encrypted key
            "ffff"  # length of the first chunk
        ) + (
            "ee"  # first encrypted chunk (65535 bytes)
        ) * 0xFFFF + (
            "0000"  # length of next (last) chunk
            "AAAA"  # invalid mac
        )))
        with self.assertRaises(RuntimeError):
            zpy.legacy.decrypt.decrypt_stream_v1("id", stdin, stdout)

    @unittest.mock.patch("zpy.legacy.decrypt.decrypt_stream_v1")
    @unittest.mock.patch("zpy.util.DecodingReader")
    def test_decrypt_stream_v1_base64(self, DecodingReader, decrypt_stream_v1):
        reader = DecodingReader.return_value.__enter__.return_value
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        zpy.legacy.decrypt.decrypt_stream_v1_base64("id", stdin, stdout)
        zpy.legacy.decrypt.decrypt_stream_v1.assert_called_once_with(
            "id", reader, stdout)
        DecodingReader.assert_called_once_with(stdin)

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("zpy.legacy.decrypt.decrypt_stream_v1_base64")
    def test_decrypt(self, decrypt_stream_v1_base64, open):
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        stdin.read.side_effect = [b"enB5", b"AAAB"]
        open.side_effect = [
            contextlib.closing(stdin),
            contextlib.closing(stdout),
        ]
        zpy.decrypt.decrypt("id", "/dev/stdin")
        self.assertEqual(open.mock_calls, [
            unittest.mock.call("/dev/stdin", "rb"),
            unittest.mock.call("/dev/stdout", "wb"),
        ])
        decrypt_stream_v1_base64.assert_called_once_with("id", stdin, stdout)

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("zpy.legacy.decrypt.decrypt_stream_v1")
    def test_decrypt_raw(self, decrypt_stream_v1, open):
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        stdin.read.side_effect = [b"zpy\x00", b"\x00\x01"]
        open.side_effect = [
            contextlib.closing(stdin),
            contextlib.closing(stdout),
        ]
        zpy.decrypt.decrypt("id", "/dev/stdin")
        self.assertEqual(open.mock_calls, [
            unittest.mock.call("/dev/stdin", "rb"),
            unittest.mock.call("/dev/stdout", "wb"),
        ])
        decrypt_stream_v1.assert_called_once_with("id", stdin, stdout)
