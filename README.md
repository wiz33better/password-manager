# Password Manager

A small command-line password manager written in Python. You set one master password, and it keeps the rest of your passwords locked away in a local SQLite database.

I built this as a learning project. I wanted to actually understand how password managers work: how a master password gets checked without being stored, how an encryption key is made from it, and how data gets locked and unlocked. So I wrote it piece by piece, tested each part as I went, and kept notes on why I wrote things the way I did.

It is not meant to replace a proper password manager like Bitwarden or KeePass. If you want something to trust with your real accounts, use one of those. If you want to see how the pieces fit together, read on.

## What it can do

- Create a master password on first run and ask for it on every run after that
- Generate random passwords (you pick upper, lower or mixed case, and whether to include numbers and symbols)
- Save entries: app or website name, username, and password
- Look up, update and delete entries
- Keep your saved passwords encrypted on disk

## How it works

The idea is simple: your master password is never stored anywhere, not even encrypted. Instead, two different things are made from it, and they do two different jobs.

**1. Checking that the master password is right (bcrypt)**
When you first set up, the master password is run through bcrypt, which produces a one-way hash with a random salt baked into it. Only that hash is saved. On later logins, whatever you type is checked against the hash. Nobody can turn the hash back into your password.

**2. Making the encryption key (PBKDF2)**
Hashing is for checking, not for encrypting, so a separate step turns your master password into a proper 32-byte key. This uses PBKDF2-HMAC with SHA-256, 480,000 iterations, and its own random 16-byte salt. That salt is saved in the database (it's not a secret), so the exact same key can be rebuilt every time you log in. The key itself is never written to disk. It only lives in memory while the program runs.

**3. Locking and unlocking passwords (Fernet)**
Saved passwords are encrypted with Fernet, which uses AES under the hood, before they go into the database. When you look one up, it's decrypted in memory using the key from step 2.

So the database only ever holds: the bcrypt hash, the PBKDF2 salt, and encrypted password blobs.

Generated passwords use Python's `secrets` module rather than `random`, since `random` isn't designed to be unpredictable enough for passwords.

## Project structure

```
password-manager/
├── main.py        # the menu and the glue that ties everything together
├── auth.py        # first-time setup and login
├── crypto.py      # hashing, key derivation, encrypt and decrypt
├── database.py    # all the SQLite code (credentials table + entries table)
├── generator.py   # random password generation
├── LICENSE
└── README.md
```

## Getting started

You'll need Python 3 and two packages:

```bash
pip install bcrypt cryptography
```

Then clone the repo and run it from inside the folder:

```bash
git clone https://github.com/wiz33better/password-manager.git
cd password-manager
python3 main.py
```

(On Windows, use `python main.py`.)

The folder needs to be one you can write to, because the program creates a `vault.db` file there on first run.

## Using it

**First run:** you'll be asked to create a master password and type it twice to confirm. You get three tries.

**After that:** you'll be asked for your master password each time you start the program. Three wrong attempts and it exits.

Once you're in, you'll see a menu:

```
1- Generate password
2- Add new entry
3- View entry
4- Update entry
5- Delete entry
6- Exit
```

- **Generate password** shows you a random 10-character password. It doesn't save it automatically, so copy it and use option 2 to store it.
- **Add new entry** asks for the app name, username and password, then encrypts and saves it.
- **View entry** searches by app name and shows the username and decrypted password for every match.
- **Update entry** lists the matches with their IDs, and you pick which ID to give a new password.
- **Delete entry** works the same way, by ID.

The reason update and delete go by ID is that you might have two accounts under the same app name (say, two Gmail accounts), and the ID is the only thing that tells them apart.

## Things to know

I'd rather be upfront about the limits:

- **App names and usernames are stored in plain text.** Only the password field is encrypted. Someone who gets your `vault.db` can't read your passwords, but they can see which services you use and your usernames. Encrypting those too would be a sensible next step (the tricky part is that searching by app name gets harder once it's encrypted).
- **Single user.** There's one master password per vault and no accounts.
- **No way to change the master password yet.** Changing it would mean re-encrypting every saved entry with a new key.
- **Your master password is the only way in.** If you forget it, the data can't be recovered. That's by design.
- **Keep `vault.db` safe.** Back it up if you care about what's in it, and don't commit it to GitHub. Add `*.db` to your `.gitignore`.
- **The generator length is fixed at 10 characters.**

## Ideas for later

- Encrypt usernames and app names as well
- Let the user choose the password length
- Offer to save a generated password straight into a new entry
- Master password change
- List all saved apps instead of searching one at a time
- Hide the master password as you type it (using `getpass`)

## What I learned

The biggest lesson was the difference between hashing and encryption. A hash is one-way and good for checking. Encryption is two-way and needs a key. I also learned why salts exist, why a key should be derived rather than stored, and why it's worth keeping each file's job small and separate.

## License

MIT. See the [LICENSE](LICENSE) file.
