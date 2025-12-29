from models.patient import Patient

class PatientController:
    def __init__(self):
        self.patients = []

    def add_patient(self, patient: Patient):
        self.patients.append(patient)

    def get_all_patients(self):
        return self.patients
