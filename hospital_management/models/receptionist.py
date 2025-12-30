from models.staff import Staff

class Receptionist(Staff):
    def __init__(self, staff_id, name, age, gender,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, "Receptionist", phone, email, address)
        self.__registered_patients = []

    def register_patient(self, patient_id):
        self.__registered_patients.append(patient_id)

    def to_dict(self):
        return {
            "id": self.person_id,
            "registered_patients": self.__registered_patients
        }