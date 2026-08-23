import os 
from crypto import hash_mp, verify_mp, derive_key
from database import save_creds, load_creds, init_db

def setup():
    chances = 0
    while chances < 3:
        password = input("Enter your password: ")
        verify = input("Enter password again to verify: ")
        if password == verify:
            hashed = hash_mp(password)
            salt = os.urandom(16)
            key = derive_key(password,salt)
            save_creds(hashed,salt)
            return key
            
        else: 
            print("Password doesnt match.")
            chances+=1
            
    else:
        print("Please try again")
    


def login():
    hashed, salt_save = load_creds()
    password = input("Enter your password to login: ")
    is_correct = verify_mp(password,hashed)
    if is_correct:
        key = derive_key(password,salt_save)
        print("Login successful")
        return key
    else:
        print("Wrong password")
        return None
