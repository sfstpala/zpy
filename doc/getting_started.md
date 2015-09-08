# Getting Started

Please note: you are testing experimental software.

## Determining if Zpy is right for you

Zpy encrypts data at rest using your ssh private key. This has implications for the
kind of security zpy provides.

- If your private key is compromised, your encrypted data is compromised too
- If you lose your private key, your data is lost too

Zpy is also not meant for communication. If you want to send encrypted files to
someone else, Zpy is not the right tool.
Consider using [GPG](https://www.gnupg.org/gph/en/manual.html) instead.

If you know about or are interested in Cryptography, read the [Theory of Operation](theory_of_operation.md).

### What should I use it for?

Again, Zpy is new, experimental software. Do not use it for anything critical.
If you are versed in cryptography, look at the source code and read the documetation
before you use it.

Here are some use-case for which zpy should work well:

- Backing up private keys, API credentials, application specific passwords
- Backing up configuration files with secrets in them
- Storing encrypted secrets on Google Drive or similar services
- Encrypting files before copying them onto removable media

### Other tools to consider

- If you are communicating with someone via email, use [GNU Privacy Guard](https://www.gnupg.org/gph/en/manual.html)
- If you are worried about your laptop being lost or storen, use [full disk encryption](https://ssd.eff.org/en/glossary/full-disk-encryption)
- If you want to chat securely, use [Cryptocat](https://crypto.cat/) or another [OTR](https://otr.cypherpunks.ca/) client
- If you want to store passwords securely, use [KeePass](http://keepass.info/)

## Installation

To install zpy, you need Python 3.4 or later.

### Debian 8, Ubuntu 14.04 or later

    # apt-get install python3-pip
    # pip3 install zpy

### Fedora 22

    # dnf install python3-pip
    # pip3 install zpy

### OS X (Homebrew)

    $ brew install python3
    $ pip3 install zpy

## Encrypting Files

To encrypt a file with, simply type:

    zpy encrypt secrets.txt

You can also pipe text into zpy:

    echo "attack at dawn" | zpy encrypt

Note that the output is Base64 encoded. If you are encrypting large files,
use the `--raw` flag to output raw bytes instead.

    zpy encrypt -r secrets.sqlite > secrets.sqlite.zpy

The location of your identity defaults to `~/.ssh/id_rsa`. If you want to
use another identity, use the `--identity` flag:

    zpy -i ~/.ssh/my_other_id encrypt secrets.txt

If your private key is encrypted with a password, you will be prompted
to enter it when you execute these commands. You can use `ssh-add` to
cache your passphrase with `ssh-agent`.

## Decrypting Files

Decrypting works the same as encrypting.

    zpy decrypt secrets.txt.zpy

The `--raw` flag is not available for decryption. Zpy will automatically
determine whether the input is binary or not.

    zpy decrypt secrets.sqlite.zpy > secrets.sqlite

If you have used a different identity for the encryption, provided it in
the same way:

    cat secrets.txt.zpy | zpy -i ~/.ssh/my_other_id decrypt

## Updating Zpy

You should regularly check for updates. Zpy encrypted files have a version
number that ensures new versions of the program can decrypt old files, but it
will only use the newest protocol for encrypting files.

To update zpy, run:

    pip install --upgrade zpy

You can find the [Changelog on GitHub](https://github.com/sfstpala/zpy/blob/master/CHANGELOG.md).
