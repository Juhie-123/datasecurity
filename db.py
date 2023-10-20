import sqlite3
from werkzeug.security import generate_password_hash

def initialize_database():
    # Connect to SQLite database (creates a new database if it doesn't exist)
    conn = sqlite3.connect('database.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL queries to create tables
    create_user_table = '''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        first_name TEXT,
        is_verified INTEGER DEFAULT 0
    );
    '''

    create_note_table = '''
    CREATE TABLE IF NOT EXISTS note (
        id INTEGER PRIMARY KEY,
        data TEXT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user (id)
    );
    '''

    # Execute the SQL queries
    cursor.execute(create_user_table)
    cursor.execute(create_note_table)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

def register_user(email, password, first_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Hash the password before storing
    hashed_password = generate_password_hash(password, method='sha256')

    # Insert the new user into the 'user' table
    cursor.execute("INSERT INTO user (email, password, first_name) VALUES (?, ?, ?)",
                   (email, hashed_password, first_name))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
