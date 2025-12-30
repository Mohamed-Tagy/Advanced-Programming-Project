from models.patient import Patient
from controllers.base_controller import BaseController

class PatientController(BaseController):
    def __init__(self):
        super().__init__()

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
        return patient

    def admit_patient(self, patient_id, admission_date, doctor_id):
        patient = self.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.admit(admission_date, doctor_id)

    def discharge_patient(self, patient_id, discharge_date, doctor_id):
        patient = self.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.discharge(discharge_date, doctor_id)

    def add_allergy(self, patient_id, allergy):
        patient = self.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.add_allergy(allergy)

    def add_medical_history(self, patient_id, condition):
        patient = self.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.add_to_medical_history(condition)

    def add_medical_note(self, patient_id, note, doctor_name):
        patient = self.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.add_medical_note(note, doctor_name)

    def get_patient(self, patient_id):
        return self.get(patient_id)
