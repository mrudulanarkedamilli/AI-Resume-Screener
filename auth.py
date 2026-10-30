
import sqlite3
import os
import hashlib
import hmac

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            salt BLOB NOT NULL,
            password_hash BLOB NOT NULL
        )
    """)
    conn.commit()
    return conn


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )


def register_user(name, email, password):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "Please fill in all fields."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    salt = os.urandom(16)
    password_hash = hash_password(password, salt)

    try:
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO users
                (name, email, salt, password_hash)
                VALUES (?, ?, ?, ?)""",
                (name, email, salt, password_hash)
            )
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "This email is already registered."


def login_user(email, password):
    email = email.strip().lower()

    with get_connection() as conn:
        user = conn.execute(
            """SELECT name, salt, password_hash
            FROM users WHERE email = ?""",
            (email,)
        ).fetchone()

    if user is None:
        return False, None

    name, salt, stored_hash = user
    entered_hash = hash_password(password, salt)

    if hmac.compare_digest(entered_hash, stored_hash):
        return True, name

    return False, None
