# database_manager.py

import sqlite3
import bcrypt

DB_NAME = "helpdesk.db"

def init_db():
    """Initialize database and create required tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            role TEXT CHECK(role IN ('student', 'admin'))
        )
    """)

    # Complaints table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            issue_type TEXT,
            description TEXT,
            status TEXT DEFAULT 'pending',
            admin_response TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()

# --- USER FUNCTIONS ---

def register_user(username, email, password, role="student"):
    """Register a new user. Returns True if success, False if user/email exists."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                       (username, email, password_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    """Fetch a user by username."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, password_hash, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "username": row[0],
            "email": row[1],
            "password_hash": row[2],
            "role": row[3]
        }
    return None

# --- COMPLAINT FUNCTIONS ---

def save_complaint(student_name, issue_type, description):
    """Save a new complaint into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO complaints (student_name, issue_type, description, status) VALUES (?, ?, ?, 'pending')",
        (student_name, issue_type, description)
    )
    conn.commit()
    conn.close()

def get_complaints():
    """Fetch all complaints from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows



def get_user_complaints(username, status=None):
    """Fetch complaints of a specific student, optionally filtered by status."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM complaints WHERE student_name = ? AND status = ? ORDER BY id DESC",
                       (username, status))
    else:
        cursor.execute("SELECT * FROM complaints WHERE student_name = ? ORDER BY id DESC", (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_complaint_status(complaint_id, status, admin_response=""):
    """Update complaint status and add admin response."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE complaints SET status = ?, admin_response = ? WHERE id = ?",
        (status, admin_response, complaint_id)
    )
    conn.commit()
    conn.close()


# --- Initialize DB when imported ---
init_db()
