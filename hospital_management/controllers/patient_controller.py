from models.patient import Patient
from controllers.base_controller import BaseController

class PatientController(BaseController):
    def __init__(self):
        self.patients = {}   # patient_id -> Patient object

    def create_patient(self, patient_id, name, age, gender,
                       blood_type=None, phone=None, email=None, address=None):
        if patient_id in self.patients:
            raise ValueError("Patient already exists")

        patient = Patient(
            patient_id, name, age, gender,
            blood_type, phone=phone, email=email, address=address
        )
        self.patients[patient_id] = patient
        return patient

    def admit_patient(self, patient_id, admission_date, doctor_id):
        patient = self.patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.admit(admission_date, doctor_id)

    def discharge_patient(self, patient_id, discharge_date, doctor_id):
        patient = self.patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.discharge(discharge_date, doctor_id)

    def get_patient(self, patient_id):
        return self.patients.get(patient_id)
