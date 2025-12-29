# database/db_manager.py
import sqlite3
from database import schema

DB_FILE = "hospital.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(schema.PATIENT_TABLE)
        self.cursor.execute(schema.STAFF_TABLE)
        self.cursor.execute(schema.APPOINTMENT_TABLE)
        self.cursor.execute(schema.BILL_TABLE)
        self.conn.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
