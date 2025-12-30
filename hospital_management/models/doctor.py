from models.person import Person

class Doctor(Person):
    def __init__(self, doctor_id, name, age, gender, specialty, license_number,
                 phone=None, email=None, address=None):
        super().__init__(doctor_id, name, age, gender, phone, email, address)
        self.specialty = specialty
        self.__license_number = license_number
        self.__patients = []
        self.__consultation_fee = 0

    @property
    def license_number(self):
        return self.__license_number

    @property
    def consultation_fee(self):
        return self.__consultation_fee

    def set_consultation_fee(self, fee):
        if fee < 0:
            raise ValueError("Consultation fee cannot be negative")
        self.__consultation_fee = fee

    def add_patient(self, patient_id):
        if patient_id not in self.__patients:
            self.__patients.append(patient_id)
            return True
        return False

    def remove_patient(self, patient_id):
        if patient_id in self.__patients:
            self.__patients.remove(patient_id)
            return True
        return False

    def get_patient_count(self):
        return len(self.__patients)

    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "specialty": self.specialty,
            "license_number": self.__license_number,
            "consultation_fee": self.__consultation_fee,
            "patients": list(self.__patients)
        }

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"
