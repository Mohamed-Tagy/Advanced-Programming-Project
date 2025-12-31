import unittest
from hospital_management.controllers.patient_controller import PatientController
from hospital_management.models.patient import Patient
from hospital_management.controllers.base_controller import BaseController
from hospital_management.database.db_manager import Database
from hospital_management.models.person import Person


class TestPatientController(unittest.TestCase):
    def setUp(self):
        self.controller = PatientController()

    def test_create_and_get_patient(self):
        patient = self.controller.create_patient(
            patient_id="P001",
            name="John Doe",
            age=30,
            gender="M",
            blood_type="A+"
        )

        self.assertEqual(patient.person_id, "P001")
        self.assertEqual(patient.name, "John Doe")

        fetched_patient = self.controller.get_patient("P001")
        self.assertEqual(fetched_patient.name, "John Doe")
        self.assertEqual(fetched_patient.blood_type, "A+")

    def test_admit_and_discharge(self):
        self.controller.create_patient(
            patient_id="P002",
            name="Jane Doe",
            age=25,
            gender="F",
            blood_type="B+"
        )

        self.controller.admit_patient("P002", "2025-12-31", "D001")
        patient = self.controller.get_patient("P002")
        self.assertTrue(patient.is_admitted())

        self.controller.discharge_patient("P002", "2026-01-02", "D001")
        patient = self.controller.get_patient("P002")
        self.assertFalse(patient.is_admitted())

    def test_allergy_and_history(self):
        self.controller.create_patient(
            patient_id="P003",
            name="Alice",
            age=28,
            gender="F",
            blood_type="O+"
        )

        self.controller.add_allergy("P003", "Peanuts")
        self.controller.add_medical_history("P003", "Asthma")

        patient = self.controller.get_patient("P003")
        self.assertIn("Peanuts", patient.to_dict()["allergies"])
        self.assertIn("Asthma", patient.to_dict()["medical_history"])

if __name__ == "__main__":
    unittest.main()
