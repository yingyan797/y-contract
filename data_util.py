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
                message_rank INTEGER,
                is_contract INTEGER,
                name TEXT,
                type TEXT,
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

    def get_ocr_texts(self, session_id):
        cursor = self._con.cursor()
        result = cursor.execute("Select * From file where session_id=?", (session_id,))
        return [{"id": r[0], "with_message": r[2], "is_contract": r[3], "file": f"[{r[5]}]-{r[4]}", "text": r[6]} for r in result.fetchall()]
    
    def get_file_contents(self, session_id):
        """
        Get all OCR processed texts for a given session.
        Returns a list of dictionaries with file name and text.
        """
        cursor = self._con.cursor()
        result = cursor.execute("Select name, type, ocr_processed_content From file where session_id=?", (session_id,))
        return [{"name": f"{r[0]}.{r[1]}", "text": r[2]} for r in result.fetchall()]
    
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
    # db("Delete from file", fetch_num=None)
    # db("DELETE FROM sqlite_sequence WHERE name='file'", fetch_num=None)
    print(db("Select session_id, name from file"))
    