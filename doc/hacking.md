# Hacking

## Setting up the development environment

Zpy is written in Python 3. To set up your development environment, you need:

- Python 3 (>= 3.4)
- The Python 3 headers (e.g. `python3-dev` on Ubuntu)
- Curl, Make, gcc or clang

The compiler and headers are required to build [PyCrypto](https://github.com/dlitz/pycrypto) from source.

On Ubuntu, type:

    sudo apt-get install build-essential curl python3-dev

The Makefile has everything you need to build a VirtualEnv so that you don't have to install anything else
on your system:

    make
    make test
    make clean

The VirtualEnv is installed in the current directory. The python interpreter is `bin/python` and zpy is
available at `bin/zpy`.

To install a release version of the program from source, build the Wheel and install it using pip:

    bin/python setup.py bdist_wheel
    sudo python3 install dist/zpy*.whl

## Tests

Note that `make test` will fail if the code coverage is not 100%. The `test` target also runs various checks.

The tests are included with the module at `zpy.tests`.

To run the test suite exactly as it runs on Travis-CI:

    tox

To run the test suite without checking code coverage:

    bin/python setup.py test
