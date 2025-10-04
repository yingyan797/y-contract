from re import L
import sqlite3, os
from tkinter import NO

class Database:
    def __init__(self, name) -> None:
        self.name = name
        if not os.path.isfile(name):
            self.start()
            self.create_schema()
            self._con.close()


    def start(self):
        self._con = sqlite3.connect(self.name)
        return self._con.cursor()

    def create_schema(self):
        """Create database schema for chatbot sessions and file info"""
        cursor = self._con.cursor()
        
        print("Initializa databse tables")
        # Session table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT DEFAULT "New Chat", 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Message table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                rank INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES session (id)
            )
        ''')
        
        # File table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                name TEXT NOT NULL,
                ocr_processed_content TEXT,
                FOREIGN KEY (session_id) REFERENCES session (id)
            )
        ''')
        
        self._con.commit()

        # Database helper functions
    def create_session(self):
        cursor = self._con.cursor()
        cursor.execute('INSERT INTO session DEFAULT VALUES')
        session_id = cursor.lastrowid
        self._con.commit()
        return session_id

    def save_message(self, session_id, role, rank, content):
        cursor = self._con.cursor()
        cursor.execute('INSERT INTO message (session_id, role, rank, content) VALUES (?, ?, ?, ?)', 
                    (session_id, role, rank, content))
        self._con.commit()
    
    def __call__(self, query, params=(), fetch_num=0):
        cursor = self._con.cursor()
        result = cursor.execute(query, params)
        if fetch_num == 0:
            return result.fetchall()
        if fetch_num == 1:
            return result.fetchone()
        else:
            self._con.commit()
        
        
if __name__ == "__main__":
    db = Database('session.db')
    db.start()
    print(db("Select * from session"))