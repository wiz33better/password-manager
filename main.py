from database import init_db, load_creds, create, retrieve, update, delete
from crypto import encrypt, decrypt
from generator import generate
from auth import setup, login

if __name__ == "__main__":
    init_db()

    if load_creds() is None:
        cap_key = setup()
        cnt = 1
    else:
        cap_key = login()
        cnt = 1

    while cnt < 3:
        if cap_key is not None:
            break
        else:
            print("Enter valid password: ")
            cnt += 1
            cap_key = login()

    if cap_key is None:
        print("Too many failed attempts. Exiting.")
        exit()

    while True:
        print("\n-------PASSWORD MANAGER---------")
        print("1- Generate password")
        print("2- Add new entry")
        print("3- View entry")
        print("4- Update entry")
        print("5- Delete entry")
        print("6- Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            case = input("Case (u/l/m): ")
            no = input("Include numbers? (y/n): ")
            sym = input("Include symbols? (y/n): ")
            new_pass = generate(case, no, sym)
            print("Generated password:", new_pass)

        elif choice == "2":
            app_name = input("App/website name: ")
            username = input("Username: ")
            raw_pass = input("Password to store: ")
            encrypted = encrypt(raw_pass, cap_key)
            create(app_name, username, encrypted)
            print("Entry saved.")

        elif choice == "3":
            app_name = input("App/website name to look up: ")
            rows = retrieve(app_name)
            if not rows:
                print("No entry found.")
            else:
                for row in rows:
                    entry_id, username, enc_pass = row
                    decrypted = decrypt(enc_pass, cap_key)
                    print(f"ID: {entry_id} | Username: {username} | Password: {decrypted}")

        elif choice == "4":
            app_name = input("App/website name to update: ")
            rows = retrieve(app_name)
            if not rows:
                print("No entry found.")
            else:
                for row in rows:
                    print(f"ID: {row[0]} | Username: {row[1]}")
                target_id = int(input("Enter the ID to update: "))
                new_raw_pass = input("New password: ")
                new_encrypted = encrypt(new_raw_pass, cap_key)
                update(target_id, new_encrypted)
                print("Entry updated.")

        elif choice == "5":
            app_name = input("App/website name to delete: ")
            rows = retrieve(app_name)
            if not rows:
                print("No entry found.")
            else:
                for row in rows:
                    print(f"ID: {row[0]} | Username: {row[1]}")
                target_id = int(input("Enter the ID to delete: "))
                delete(target_id)
                print("Entry deleted.")

        elif choice == "6":
            print("See you again!")
            break

        else:
            print("Invalid choice, try again.")
