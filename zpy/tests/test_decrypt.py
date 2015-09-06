import unittest
import unittest.mock
import io
import binascii
import contextlib
import zpy.decrypt


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
        zpy.decrypt.decrypt_stream_v1("id", stdin, stdout)
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
            zpy.decrypt.decrypt_stream_v1("id", stdin, stdout)

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("zpy.decrypt.decrypt_stream_v1")
    def test_decrypt(self, decrypt_stream_v1, open):
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        stdin.read.side_effect = [b"zpy\x01"]
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

    @unittest.mock.patch("builtins.open")
    def test_decrypt_invalid_header(self, open):
        stdin, stdout = unittest.mock.Mock(), unittest.mock.Mock()
        stdin.read.side_effect = [b"\x00\x00\x00\x00"]
        open.side_effect = [
            contextlib.closing(stdin),
            contextlib.closing(stdout),
        ]
        with self.assertRaises(RuntimeError):
            zpy.decrypt.decrypt("id", "/dev/stdin")
        self.assertEqual(open.mock_calls, [
            unittest.mock.call("/dev/stdin", "rb"),
            unittest.mock.call("/dev/stdout", "wb"),
        ])
