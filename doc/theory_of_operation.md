# Theory of Operation

This document describes the details of the encryption process and how Zpy reads and write files.

## Encryption

### Version 1

TBD

## Decryption

### Version 1

TBD

## File Format

### Encoding

Zpy encrypted files are either a stream of raw bytes or a [base64 encoded](https://tools.ietf.org/html/rfc3548)
version of that stream. Every file starts with 6 magic bytes, the first three of which are `zpy` and the last
three are a version number for the decryption protocol. If the file is base64 encoded, the magic bytes are
contained in the first eight characters.

### Version 1

Version 1 files start with the following bytes:

    7a 70 79 00 00 01

Which is `enB5AAAB` in base64.

Next is the length of the encrypted symmetric key (big endian, two bytes) followed by the encrypted key itself:

    01 00
    XX XX XX XX ... [256 bytes]

Next is a variable number of ciphertext chunk. Each chunk starts with its length (big endian, two bytes). The
end of the ciphertext stream is signified by a chunk of length zero. The example shows the ciphertext stream
for a ~128 KiB file:

    FF FF
    XX XX XX XX ... [65535 bytes]
    FF FF
    XX XX XX XX ... [65535 bytes]
    00 CA
    XX XX XX XX ... [202 bytes]
    00 00

The last 32 bytes are the HMAC digest of the file after encryption without a length indicator:

    XX XX XX XX ... [32 bytes]
