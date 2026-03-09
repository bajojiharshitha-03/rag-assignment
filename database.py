import sqlite3

def create_db():
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk TEXT,
        embedding TEXT
    )
    """)

    conn.commit()
    conn.close()

create_db()