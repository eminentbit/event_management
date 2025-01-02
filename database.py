import sqlite3

def connect_database():
    # Connect to the database (or create one if it doesn't exist)
    connection = sqlite3.connect("users.db")

    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Create a sample table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        picture TEXT
    )
    """)

    # Create Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            venue TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

    # Commit changes and close the connection
    connection.commit()
    connection.close()