import pyodbc
import time

class Database:
    def __init__(self):
        # Update connection string to use trusted connection
        self.conn_str = (
            'DRIVER={ODBC Driver 17 for SQL Server};'  # Updated driver name
            'SERVER=(local);'  # Use (local) instead of localhost
            'DATABASE=TodoNotesDB;'
            'Trusted_Connection=yes;'  # Use Windows Authentication
            'timeout=30;'  # Add connection timeout
        )
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        self.init_db()
    
    def get_connection(self):
        for attempt in range(self.max_retries):
            try:
                return pyodbc.connect(self.conn_str)
            except pyodbc.Error as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to connect after {self.max_retries} attempts: {str(e)}")
                time.sleep(self.retry_delay)
    
    def init_db(self):
        try:
            # Connect to master database first
            master_conn_str = (
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=(local);'
                'DATABASE=master;'
                'Trusted_Connection=yes;'
                'timeout=30;'
            )
            
            master_conn = pyodbc.connect(master_conn_str)
            cursor = master_conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TodoNotesDB')
                BEGIN
                    CREATE DATABASE TodoNotesDB;
                END
            """)
            master_conn.commit()
            cursor.close()
            master_conn.close()

            # Now connect to our database and create tables
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create todos table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[todos]') AND type in (N'U'))
                BEGIN
                    CREATE TABLE todos (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        task NVARCHAR(500) NOT NULL,
                        link NVARCHAR(1000),
                        created_at DATETIME DEFAULT GETDATE()
                    )
                END
            """)
            
            # Create notes table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[notes]') AND type in (N'U'))
                BEGIN
                    CREATE TABLE notes (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        title NVARCHAR(200) NOT NULL,
                        content NVARCHAR(MAX),
                        pinned BIT DEFAULT 0,
                        created_at DATETIME DEFAULT GETDATE()
                    )
                END
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            raise Exception(f"Database initialization failed: {str(e)}")

    def add_todo(self, task, link):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO todos (task, link) VALUES (?, ?)", (task, link))
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to add todo: {str(e)}")

    def get_todos(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, task, link FROM todos ORDER BY created_at DESC")
            todos = cursor.fetchall()
            cursor.close()
            conn.close()
            return todos
        except pyodbc.Error as e:
            raise Exception(f"Failed to get todos: {str(e)}")

    def update_todo(self, todo_id, task):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE todos SET task = ? WHERE id = ?", (task, todo_id))
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to update todo: {str(e)}")

    def delete_todo(self, todo_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to delete todo: {str(e)}")

    def add_note(self, title, content):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to add note: {str(e)}")

    def get_notes(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content, pinned FROM notes ORDER BY pinned DESC, created_at DESC")
            notes = cursor.fetchall()
            cursor.close()
            conn.close()
            return notes
        except pyodbc.Error as e:
            raise Exception(f"Failed to get notes: {str(e)}")

    def update_note(self, note_id, title):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET title = ? WHERE id = ?", (title, note_id))
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to update note: {str(e)}")

    def delete_note(self, note_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to delete note: {str(e)}")

    def toggle_note_pin(self, note_id, pinned):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET pinned = ? WHERE id = ?", (pinned, note_id))
            conn.commit()
            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to toggle note pin: {str(e)}")