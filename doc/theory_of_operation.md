# Theory of Operation

This document describes the details of the encryption process and how Zpy reads and write files.

## Encryption

### Version 1

The encryption is RSA with AES-256-CTR and HMAC-SHA256.

Zpy will initialize a secure random number generator (using `/dev/urandom`) and generate the following:

- 16 byte initialization vector
- 32 byte random symmetric key

It will then generate an AES Counter object, the initial value of which is the IV generated earlier, and
an HMAC-SHA256 object with the 32 byte random symmetric key.

Next we load the users SSH key pair and use the public key to encrypt the symmetric key, giving us the
encrypted symmetric key.

We output the IV and the encrypted symmetric key.

The data is then encrypted using AES256 in counter mode and with the random symmetric key. There is no
additional padding.

We output the encrypted chunks.

The HMAC is updated with every encrypted chunk (*Encrypt-then-MAC*). The last step is to output the
HMAC digest.

### Version 2

Version 2 is exactly like version one, except:

- Instead of 32 random bytes for the symmetric encryption key, we generate 64 bytes.

The first half of the key is used for the AES encryption, the second half is used
for the HMAC-SHA256 authentication

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

### Version 2

Version 2 files start with the following bytes:

    7a 70 79 00 00 02

Which is `enB5AAAC` in base64.
