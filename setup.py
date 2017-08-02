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

import os.path
import setuptools


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "DESCRIPTION.rst")) as f:
    long_description = f.read()

setuptools.setup(
    name="zpy", version="0.4.0",
    description="Quickly encrypt files with your ssh identity",
    long_description=long_description,
    packages=setuptools.find_packages(),
    test_suite="zpy.tests",
    author="Stefano Palazzo",
    author_email="stefano.palazzo@gmail.com",
    url="https://github.com/sfstpala/zpy",
    zip_safe=False,
    license="GPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: " + (
            "GNU Lesser General Public License v3 or later (LGPLv3+)"),
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
    ],
    install_requires=[
        "docopt",
        "pycrypto",
    ],
    entry_points={
        "console_scripts": [
            "zpy = zpy.__main__:main",
        ]
    },
)
