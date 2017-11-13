# Blatantly ripped off of Fernet from cryptography

# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import absolute_import, division, print_function

import base64
import binascii
import os
import struct
import time

import six

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
import datetime
# as pad


class InvalidToken(Exception):
    pass


_MAX_CLOCK_SKEW = 60


class Potamus(object):
    def __init__(self, key, backend=None):
        if backend is None:
            backend = default_backend()

        key = base64.urlsafe_b64decode(key)
        if len(key) != 32:
            raise ValueError(
                "Potamus key must be 32 url-safe base64-encoded bytes."
            )

        self._signing_key = key[:16]
        self._encryption_key = key[16:]
        self._backend = backend

    @classmethod
    def generate_key(cls):
        return base64.urlsafe_b64encode(os.urandom(32))

    def encrypt(self, data):
        current_time = int(time.time())
        iv = os.urandom(16)
        return self._encrypt_from_parts(data, current_time, iv)

    def _encrypt_from_parts(self, data, current_time, iv):
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes.")

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encryptor = Cipher(
            algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend
        ).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        basic_parts = (
            b"\x80" + struct.pack(">Q", current_time) + iv + ciphertext
        )

        h = HMAC(self._signing_key, hashes.SHA256(), backend=self._backend)
        h.update(basic_parts)
        hmac = h.finalize()
        return base64.urlsafe_b64encode(basic_parts + hmac)

    def decrypt(self, token, ttl=None):
        if not isinstance(token, bytes):
            raise TypeError("token must be bytes.")

        current_time = int(time.time())

        try:
            data = base64.urlsafe_b64decode(token)
        except (TypeError, binascii.Error):
            raise InvalidToken

        if not data or six.indexbytes(data, 0) != 0x80:
            raise InvalidToken

        try:
            timestamp, = struct.unpack(">Q", data[1:9])
        except struct.error:
            raise InvalidToken
        if ttl is not None:
            if timestamp + ttl < current_time:
                raise InvalidToken

            if current_time + _MAX_CLOCK_SKEW < timestamp:
                raise InvalidToken

        h = HMAC(self._signing_key, hashes.SHA256(), backend=self._backend)
        h.update(data[:-32])
        try:
            h.verify(data[-32:])
        except InvalidSignature:
            raise InvalidToken

        iv = data[9:25]
        ciphertext = data[25:-32]
        decryptor = Cipher(
            algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend
        ).decryptor()
        plaintext_padded = decryptor.update(ciphertext)
        try:
            plaintext_padded += decryptor.finalize()
        except ValueError:
            raise InvalidToken
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

        unpadded = unpadder.update(plaintext_padded)
        try:
            unpadded += unpadder.finalize()
        except ValueError:
            raise InvalidToken
        return unpadded


class MultiPotamus(object):
    def __init__(self, fernets):
        fernets = list(fernets)
        if not fernets:
            raise ValueError(
                "MultiPotamus requires at least one Potamus instance"
            )
        self._fernets = fernets

    def encrypt(self, msg):
        return self._fernets[0].encrypt(msg)

    def decrypt(self, msg, ttl=None):
        for f in self._fernets:
            try:
                return f.decrypt(msg, ttl)
            except InvalidToken:
                pass
        raise InvalidToken


class AsyPotamus(object):
    private_key = None
    public_key = None
    cert = None

    def __init__(self):
        self.genkeys()

    def genkeys(self):
        one_day = datetime.timedelta(1, 0, 0)
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
        self.public_key = self.private_key.public_key()
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u'cryptopotamus.org')]))
        builder = builder.issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u'cryptopotamus.org')]))
        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime(2018, 8, 2))
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.public_key(self.public_key)
        self.cert = builder.sign(private_key=self.private_key, algorithm=hashes.SHA256(), backend=default_backend())

    def serialized_cert(self):
        return self.cert.public_bytes(encoding=serialization.Encoding.PEM)

    def write_key_and_cert(self, certname="cert.pem", keyname="key.pem"):
        with open(certname, "wb") as f:
            f.write(self.cert.public_bytes(serialization.Encoding.PEM))
        with open(keyname, "wb") as f:
            f.write(self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                   format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                   encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),))
