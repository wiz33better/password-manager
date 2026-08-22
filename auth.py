import os 
from crypto import hash_mp
from crypto import verify_mp
from crypto import derive_key

def setup():
    chances = 0
    while chances < 3:
        password = input("Enter your password: ")
        verify = input("Enter password again to verify: ")
        if password == verify:
            hashed = hash_mp(password)
            salt = os.urandom(16)
            key = derive_key(password,salt)
            creds(hashed,salt)
            return key
            
        else: 
            print("Password doesnt match.")
            chances+=1
            return None
    else:
        print("Please try again")
    

def creds(hashed, salt):
    print("Password: ",hashed)
    salt_save = salt
    return salt_save

def login(hashed, salt_save):
    password = input("Enter your password: ")
    is_correct = verify_mp(password,hashed)
    if is_correct:
        key = derive_key(password,salt_save)
        return key
    else:
        print("Wrong password")
        return None

if __name__ == "__main__":
    setup()
    login()
