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

def encrypt(key,plaintext):
    f = Fernet(base64.urlsafe_b64encode(key))
    encoded = plaintext.encode()
    encrypted = f.encrypt(encoded)    
    return encrypted
    
if __name__ == "__main__":
    password = input("Enter a password:")
    salt = os.urandom(16)
    key1 = derive_key(password,salt)
    encrypt_check = encrypt(key1, password)
    print(encrypt_check)
    hashed = hash_mp(password)
    print(hashed)
    password = input("Enter password to verify:")
    verify = verify_mp(password,hashed)
    print(verify)


##def decrypt(pasword,key):