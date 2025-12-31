import sqlite3

class BaseController:
    def __init__(self, db_path="hospital.db"):
        self.db_path = db_path
        self._items = {}

    def _get_connection(self):
        """Creates a fresh connection per request to prevent threading conflicts."""
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def execute_query(self, query, params=()):
        """Use for SELECT statements. Returns all results."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_non_query(self, query, params=()):
        """Use for INSERT, UPDATE, DELETE. Returns True if successful."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
            
    def exists(self, table, column, value):
        """Generic existence check useful for all controllers."""
        query = f"SELECT 1 FROM {table} WHERE {column} = ?"
        result = self.execute_query(query, (value,))
        return len(result) > 0