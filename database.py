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
