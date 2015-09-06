import unittest
import unittest.mock
import io
import binascii
import contextlib
import zpy.encrypt


class EncryptTest(unittest.TestCase):

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("Crypto.Random.new")
    @unittest.mock.patch("Crypto.PublicKey.RSA.importKey")
    @unittest.mock.patch("Crypto.Cipher.AES.new")
    @unittest.mock.patch("Crypto.Cipher.PKCS1_OAEP.new")
    @unittest.mock.patch("Crypto.Util.Counter.new")
    @unittest.mock.patch("Crypto.Hash.HMAC.new")
    def test_encrypt_stream_v1(
            self, new_HMAC, new_Counter, new_PKCS1_OAEP, new_AES,
            importKey, new_Random, open):
        f = unittest.mock.Mock()
        f.read.return_value = b""
        open.side_effect = lambda fn: contextlib.closing(f)
        stdin = io.BytesIO(b"\xEE" * 0xFFFF)
        stdout = io.BytesIO()
        iv = b"\x00" * 8
        key = b"\xFF" * 32
        new_Random.return_value = io.BytesIO(iv + key)
        new_PKCS1_OAEP.return_value.encrypt.return_value = b"\xAA"
        new_AES.return_value.encrypt.side_effect = lambda x: x
        new_HMAC.return_value.digest.return_value = b"\xCC"
        zpy.encrypt.encrypt_stream_v1("id", stdin, stdout)
        counter = new_Counter.return_value
        new_AES.assert_called_once_with(key, mode=6, counter=counter)
        importKey.assert_called_once_with(b"")
        open.assert_called_once_with("id")
        res = binascii.hexlify(stdout.getvalue()).decode()
        self.assertEqual(res[:26], (
            "0000000000000000"  # iv
            "0001"  # length of encrypted key
            "aa"  # encrypted key
            "ffff"  # length of the first chunk
        ))
        self.assertEqual(res[26:-6], (
            "ee"  # first encrypted chunk (65535 bytes)
        ) * 0xFFFF)
        self.assertEqual(res[-6:], (
            "0000"  # length of next (last) chunk
            "cc"  # mac
        ))

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("zpy.encrypt.encrypt_stream_v1")
    def test_encrypt(self, encrypt_stream_v1, open):
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
        encrypt_stream_v1.assert_called_once_with("id", stdin, stdout)
        stdout.write.assert_called_once_with(b"zpy\x01")

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
