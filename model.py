import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        '''
    )
    conn.commit()

    # Insert sample users if table empty
    cur.execute('SELECT COUNT(1) as cnt FROM users')
    row = cur.fetchone()
    if row and row['cnt'] == 0:
        create_user('alice', 'password123')
        create_user('bob', 'secret')
    conn.close()


def create_user(username, password):
    pw_hash = generate_password_hash(password)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, pw_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    return row


def verify_user(username, password):
    row = get_user(username)
    if not row:
        return False
    return check_password_hash(row['password'], password)
