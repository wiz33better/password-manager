import bcrypt
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from cryptography.fernet import Fernet

def hash_mp(password):
    encoded = password.encode()
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(encoded,salt)
    return hashed_pass

def verify_mp(password1,hashed_pass):
    encoded = password1.encode()
    return bcrypt.checkpw(encoded,hashed_pass)

def derive_key(password,psalt):
    encoded = password.encode()
    kdf = PBKDF2HMAC(
        algorithm= hashes.SHA256(),
        length=32,
        salt=psalt,
        iterations=480000,
    )
    key = kdf.derive(encoded)
    return key

def encrypt(plaintext, key):
    f = Fernet(base64.urlsafe_b64encode(key))
    encoded = plaintext.encode()
    encrypted = f.encrypt(encoded)
    return encrypted

def decrypt(encrypted,key):
    f = Fernet(base64.urlsafe_b64encode(key))
    decrypted = f.decrypt(encrypted)
    decoded = decrypted.decode()
    return decoded
