# Zpy

[![Build](https://img.shields.io/travis/sfstpala/zpy.svg?style=flat-square)](https://travis-ci.org/sfstpala/zpy)
[![Coverage](https://img.shields.io/coveralls/sfstpala/zpy.svg?style=flat-square)](https://coveralls.io/r/sfstpala/zpy)

Quickly encrypt files with your ssh identity.

Note: **This is experimental software!**

## Development setup

Type `make test` to build zpy in a virtualenv and run the test suite.  
Afte running `make`, you can run zpy by typing `bin/zpy`.

Prerequisites are make, curl, python (3.4 or newer), and openssl.

## Usage

    Usage:
        zpy [options] encrypt [<filename>] [-r]
        zpy [options] decrypt [<filename>]
        zpy (--help | --copying | --version)

See [`__main__.py`](zpy/__main__.py) for more info.

## Copyright notice

Copyright (C) 2015  Stefano Palazzo <stefano.palazzo@gmail.com>

This program comes with ABSOLUTELY NO WARRANTY;  
This is free software, and you are welcome to redistribute it  
under certain conditions; see [COPYING](COPYING) for details.
