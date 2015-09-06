import unittest
import unittest.mock
import io
import contextlib
import zpy.util


class UtilTest(unittest.TestCase):

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("Crypto.PublicKey.RSA.importKey")
    def test_load_identity(self, importKey, open):
        open.return_value = contextlib.closing(io.BytesIO(b"..."))
        self.assertEqual(zpy.util.load_identity("id"), importKey.return_value)
        open.assert_called_once_with("id")
        importKey.assert_called_once_with(b"...")

    @unittest.mock.patch("builtins.open")
    @unittest.mock.patch("subprocess.check_output")
    @unittest.mock.patch("Crypto.PublicKey.RSA.importKey")
    def test_load_identity_encrypted(self, importKey, check_output, open):
        open.return_value = contextlib.closing(io.BytesIO(b"..."))
        key = unittest.mock.Mock()
        importKey.side_effect = [ValueError(), key]
        check_output.return_value = b"..."
        self.assertEqual(zpy.util.load_identity("id"), key)
        open.assert_called_once_with("id")
        check_output.assert_called_once_with(["openssl", "rsa", "-in", "id"])
        self.assertEqual(importKey.mock_calls, [
            unittest.mock.call(b"..."),
            unittest.mock.call(b"..."),
        ])
