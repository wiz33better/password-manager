import sqlite3

def init_db():
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
        hash BLOB,
        salt BLOB
        );
    
        """
    )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app TEXT,
        username TEXT,
        password BLOB
        );
        """
    )
    conn.commit()
    conn.close()

def save_creds(hash, salt):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credentials (hash, salt) VALUES (?, ?)", (hash, salt))
    conn.commit()
    conn.close()

def load_creds():
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT hash, salt FROM credentials")
    row = cursor.fetchone() 
    conn.close()
    return row

def create(app,username,e_pass):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entries (app, username, password) VALUES (?, ?, ?)", (app, username,e_pass))
    conn.commit()
    conn.close()
def retrieve(app):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id,username, password FROM entries WHERE app = ?",(app,))
    row1 = cursor.fetchall() 
    conn.close()
    return row1
def update(target_id,password):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE entries SET password = ? WHERE id = ?", (password, target_id))
    conn.commit()
    conn.close()
def delete(target_id):
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE id = ?", (target_id,))
    conn.commit()
    conn.close()

