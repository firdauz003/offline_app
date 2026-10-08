import sqlite3
from pathlib import Path

# Folder containing this Python file
APP_FOLDER = Path(__file__).parent

# Database file inside the project folder
DATABASE_FILE = APP_FOLDER / "app_data.db"


def create_database():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_note(text):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO notes (text) VALUES (?)",
        (text,)
    )

    connection.commit()
    connection.close()


def get_notes():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT id, text FROM notes")
    notes = cursor.fetchall()

    connection.close()
    return notes