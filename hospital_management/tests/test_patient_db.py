import unittest
import os
from hospital_management.database.db_manager import Database
from hospital_management.database import schema

TEST_DB = os.path.join(os.path.dirname(__file__), "test_hospital.db")

class TestPatientDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global DB_FILE
        DB_FILE = TEST_DB  
        cls.db = Database()  

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_insert_and_fetch_patient(self):
        insert_query = "INSERT INTO patients (id, name, age) VALUES (?, ?, ?)"
        self.db.execute(insert_query, (1, "Ahmed", 25))

        select_query = "SELECT * FROM patients WHERE id = ?"
        patient = self.db.fetchone(select_query, (1,))
        self.assertIsNotNone(patient)
        self.assertEqual(patient[1], "Ahmed")
        self.assertEqual(patient[2], 25)

if __name__ == "__main__":
    unittest.main()
