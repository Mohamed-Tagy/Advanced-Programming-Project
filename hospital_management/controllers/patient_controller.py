from hospital_management.models.patient import Patient
from hospital_management.controllers.base_controller import BaseController
from hospital_management.database.db_manager import Database


class PatientController(BaseController):
    def __init__(self):
        super().__init__()
        self.db = Database()

    def create_patient(self, patient_id, name, age, gender,
                       blood_type=None, allergies=None, medical_history=None,
                       phone=None, email=None, address=None):
        if self.exists(patient_id):
            raise ValueError("Patient already exists")

        patient = Patient(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            blood_type=blood_type,
            allergies=allergies,
            medical_history=medical_history,
            phone=phone,
            email=email,
            address=address
        )

        self._items[patient_id] = patient

        self.db.execute(
    "INSERT INTO patients (patient_id, name, age, gender, blood_type) VALUES (?, ?, ?, ?, ?)",
    (patient_id, name, age, gender, blood_type)
)


        return patient

    def get_patient(self, patient_id):
        if patient_id in self._items:
            return self._items[patient_id]

        row = self.db.fetchone(
    "SELECT patient_id, name, age, gender, blood_type FROM patients WHERE patient_id=?",
    (patient_id,)
)

        if row:
            patient = Patient(
                patient_id=row[0],
                name=row[1],
                age=row[2],
                gender=row[3],
                blood_type=row[4]
            )
            self._items[patient_id] = patient
            return patient
        return None


    def admit_patient(self, patient_id, admission_date, doctor_id):
        patient = self.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.admit(admission_date, doctor_id)

    def discharge_patient(self, patient_id, discharge_date, doctor_id):
        patient = self.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.discharge(discharge_date, doctor_id)

    def add_allergy(self, patient_id, allergy):
        patient = self.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.add_allergy(allergy)

    def add_medical_history(self, patient_id, condition):
        patient = self.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.add_to_medical_history(condition)

    def add_medical_note(self, patient_id, note, doctor_name):
        patient = self.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.add_medical_note(note, doctor_name)
