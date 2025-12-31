import sqlite3
from backend.database import schema

DB_FILE = "hospital.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.create_tables()
        self.apply_migrations() 

    def create_tables(self):
        with self.conn:
            self.conn.execute(schema.PATIENT_TABLE)
            self.conn.execute(schema.STAFF_TABLE)
            if hasattr(schema, 'DOCTOR_TABLE') and schema.DOCTOR_TABLE: 
                self.conn.execute(schema.DOCTOR_TABLE)
            if hasattr(schema, 'ADMIN_TABLE') and schema.ADMIN_TABLE: 
                self.conn.execute(schema.ADMIN_TABLE)
            self.conn.execute(schema.APPOINTMENT_TABLE)
            self.conn.execute(schema.BILL_TABLE)

    def apply_migrations(self):
        """Checks for missing columns in existing tables and adds them."""
        try:
            cursor = self.conn.execute("PRAGMA table_info(appointments)")
            app_columns = [info[1] for info in cursor.fetchall()]
            
            if "status" not in app_columns:
                with self.conn:
                    self.conn.execute("ALTER TABLE appointments ADD COLUMN status TEXT DEFAULT 'Scheduled'")
            
            if "notes" not in app_columns:
                with self.conn:
                    self.conn.execute("ALTER TABLE appointments ADD COLUMN notes TEXT")

            cursor = self.conn.execute("PRAGMA table_info(patients)")
            pat_columns = [info[1] for info in cursor.fetchall()]
            
            if "admitted" not in pat_columns:
                print("Migration: Adding 'admitted' column to patients table...")
                with self.conn:
                    self.conn.execute("ALTER TABLE patients ADD COLUMN admitted INTEGER DEFAULT 0")

            if "status" not in pat_columns:
                with self.conn:
                    self.conn.execute("ALTER TABLE patients ADD COLUMN status TEXT DEFAULT 'Active'")

            if "last_admission" not in pat_columns:
                with self.conn:
                    self.conn.execute("ALTER TABLE patients ADD COLUMN last_admission TEXT")

            cursor = self.conn.execute("PRAGMA table_info(staff)")
            staff_columns = [info[1] for info in cursor.fetchall()]

            if "status" not in staff_columns:
                print("Migration: Adding 'status' column to staff table...")
                with self.conn:
                    self.conn.execute("ALTER TABLE staff ADD COLUMN status TEXT DEFAULT 'Active'")

            if "fee" not in staff_columns:
                print("Migration: Adding 'fee' column to staff table...")
                with self.conn:
                    self.conn.execute("ALTER TABLE staff ADD COLUMN fee REAL DEFAULT 0.0")

        except sqlite3.Error as e:
            print(f"Migration Error: {e}")

    def execute(self, query, params=()):
        """For INSERT, UPDATE, DELETE actions."""
        try:
            with self.conn:
                cursor = self.conn.execute(query, params)
                return cursor
        except sqlite3.Error as e:
            print(f"Database Execute Error: {e}")
            raise e

    def fetchall(self, query, params=()):
        """For fetching multiple rows."""
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database FetchAll Error: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def fetchone(self, query, params=()):
        """For fetching a single row."""
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database FetchOne Error: {e}")
            return None
        finally:
            if cursor: cursor.close()

    def close(self):
        self.conn.close()