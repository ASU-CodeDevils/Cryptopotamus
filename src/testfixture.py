import os
from OpenSSL import SSL, crypto

CRT_PATH = "../scache/crt.pem"  # self-signed certificate
KEY_PATH = "../scache/key.pem"  # private key used to sign the certificate


def generate_key():
    """
    Generate a private key and dump it to the key file.
    :return: key
    """
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 4096)
    with open(KEY_PATH, "w") as keyfile:
        keyfile.write(bytes.decode(crypto.dump_privatekey(crypto.FILETYPE_PEM, key)))
    return key


def generate_crt(key):
    """
    Generate a self-signed certificate.
    :return: certificate
    """
    crt = crypto.X509()
    crt.get_subject().C = "US"
    crt.get_subject().ST = "Arizona"
    crt.get_subject().L = "Tempe"
    crt.get_subject().O = "Arizona State University"
    crt.get_subject().OU = "CodeDevils"
    crt.get_subject().CN = "localhost"
    crt.set_pubkey(key)
    crt.set_serial_number(101010)
    crt.gmtime_adj_notBefore(0)
    crt.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    crt.sign(key, 'sha256')  # Self-sign
    with open(CRT_PATH, "w") as crtfile:
        crtfile.write(bytes.decode(crypto.dump_certificate(crypto.FILETYPE_PEM, crt)))
    return crt


if __name__ == "__main__":
    generate_crt(generate_key())
