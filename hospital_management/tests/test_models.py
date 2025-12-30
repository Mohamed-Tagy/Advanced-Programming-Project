import unittest
from hospital_management.models.person import Person
from hospital_management.models.staff import Staff
from hospital_management.models.patient import Patient

class TestModels(unittest.TestCase):
    def test_person_creation(self):
        p = Person(name="John Doe", age=30)
        self.assertEqual(p.name, "John Doe")
        self.assertEqual(p.age, 30)

    def test_staff_creation(self):
        s = Staff(name="Alice", role="Nurse")
        self.assertEqual(s.role, "Nurse")

    def test_patient_creation(self):
        pat = Patient(name="Bob", ailment="Flu")
        self.assertEqual(pat.ailment, "Flu")

if __name__ == "__main__":
    unittest.main()
