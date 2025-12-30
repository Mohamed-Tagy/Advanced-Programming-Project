from models.staff import Staff
class Nurse(Staff):
    def __init__(self, staff_id, name, age, gender, department,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, "Nurse", phone, email, address)
        self.department = department
        self.__assigned_patients = []

    def assign_patient(self, patient_id):
        self.__assigned_patients.append(patient_id)

    def to_dict(self):
        return {
            "id": self.person_id,
            "department": self.department,
            "patients": self.__assigned_patients
        }
