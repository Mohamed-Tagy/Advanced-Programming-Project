import sqlite3
from sqlite3 import Error
from utils.config import DB_PATH


class Database:
    def __init__(self):
    
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
      
        try:
            self.connection = sqlite3.connect(DB_PATH)
            self.cursor = self.connection.cursor()
            print("Database connected successfully.")
        except Error as e:
            print(f"Database connection failed: {e}")

    def execute(self, query, params=()):
       
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Database execution error: {e}")

    def fetch_one(self, query, params=()):
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Error as e:
            print(f"Database fetch_one error: {e}")
            return None

    def fetch_all(self, query, params=()):
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Database fetch_all error: {e}")
            return []

    def create_tables(self):
        
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        patients_table = """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        doctors_table = """
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            specialization TEXT,
            phone TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        self.execute(users_table)
        self.execute(patients_table)
        self.execute(doctors_table)

    def close(self):
      
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
