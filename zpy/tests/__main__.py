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
    def test_copying(self, print):
        self.assertEqual(self.main(["--copying"]), 0)
        print.assert_called_once_with(zpy.__copying__)

    @unittest.mock.patch("builtins.print")
    def test_invalid_argument(self, print):
        self.assertEqual(self.main(["--invalid-argument"]), 2)
        print.assert_called_once_with(
            zpy.__main__.__doc__.split("\n\n")[1].strip(), file=sys.stderr)


if __name__ == "__main__":
    os.chdir(os.path.split(os.path.split(zpy.__file__)[0])[0])
    sys.exit(os.system(sys.executable + " setup.py test"))
