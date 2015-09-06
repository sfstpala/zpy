import unittest
import unittest.mock
import sys
import os.path
import pkg_resources
import zpy
import zpy.__main__


class EntryPointTest(unittest.TestCase):

    dist = pkg_resources.get_distribution("zpy")
    main = staticmethod(dist.load_entry_point("console_scripts", "zpy"))

    @unittest.mock.patch("zpy.encrypt.encrypt")
    def test_encryt(self, encrypt):
        encrypt.return_value = 0
        self.assertEqual(self.main(["encrypt"]), 0)

    @unittest.mock.patch("zpy.decrypt.decrypt")
    def test_decryt(self, decrypt):
        decrypt.return_value = 0
        self.assertEqual(self.main(["decrypt"]), 0)

    @unittest.mock.patch("docopt.docopt")
    def test_main(self, docopt):
        docopt.return_value = {}
        self.assertEqual(self.main([]), 0)

    @unittest.mock.patch("builtins.print")
    def test_invalid_argument(self, print):
        self.assertEqual(self.main(["--invalid-argument"]), 2)
        print.assert_called_once_with(
            zpy.__main__.__doc__.split("\n\n")[0].strip(), file=sys.stderr)


if __name__ == "__main__":
    os.chdir(os.path.split(os.path.split(zpy.__file__)[0])[0])
    sys.exit(os.system(sys.executable + " setup.py test"))
