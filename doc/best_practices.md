# Best Practices

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

## Miscellaneous

- You should clone this repository on the machine where your private key is stored in case there is a problem with PyPI or GitHub.
