import os
from cryptography.hazmat.primitives import hashes, padding, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

backend = default_backend()

def derive_key(password: bytes, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    return kdf.derive(password)

def encrypt(data, key):
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv + ciphertext


def decrypt(data, key):
    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def generate_hmac(data, key):
    h = hmac.HMAC(key, hashes.SHA256(), backend=backend)
    h.update(data)
    return h.finalize()


def verify_hmac(data, key, tag):
    h = hmac.HMAC(key, hashes.SHA256(), backend=backend)
    h.update(data)
    h.verify(tag)