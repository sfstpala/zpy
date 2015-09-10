# Zpy

[![Build](https://img.shields.io/travis/sfstpala/zpy.svg?style=flat-square)](https://travis-ci.org/sfstpala/zpy)
[![Coverage](https://img.shields.io/coveralls/sfstpala/zpy.svg?style=flat-square)](https://coveralls.io/r/sfstpala/zpy)
[![PyPI](https://img.shields.io/pypi/v/zpy.svg?style=flat-square)](https://pypi.python.org/pypi/pcr)

Quickly encrypt files with your ssh identity.

Note: **This is experimental software!**

## Links

 - [**Download**](https://pypi.python.org/pypi/zpy)
 - [**Changelog**](CHANGELOG.md)
 - [**Builds on Travis-CI**](https://travis-ci.org/sfstpala/zpy)

## Installation

The easiest way to install zpy is via PyPI:

    pip3 install zpy

You need to have Python 3.4 (or later) installed. You also need OpenSSL if your SSH private key is encrypted.

The releases are signed with PGP. You can find my public key at [palazzo.link](https://palazzo.link).

## Development setup

Install the prerequisites:

    sudo apt-get install build-essential curl python3-dev

Then run the test suite:

    make test

Afte running `make`, you can run zpy by typing `bin/zpy`.

## Copyright notice

Copyright (C) 2015  Stefano Palazzo <stefano.palazzo@gmail.com>

This program comes with ABSOLUTELY NO WARRANTY;  
This is free software, and you are welcome to redistribute it  
under certain conditions; see [COPYING](COPYING) for details.
