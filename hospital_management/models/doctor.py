from models.staff import Staff
class Doctor(Staff):
    def __init__(self, doctor_id, name, age, gender, specialty, license_number,
                 phone=None, email=None, address=None):
        super().__init__(doctor_id, name, age, gender, "Doctor", phone, email, address)

        self.specialty = specialty
        self.__license_number = license_number          # sensitive
        self.__patients = []
        self.__consultation_fee = 0                     # controlled

    # -------- LICENSE (READ-ONLY) --------
    @property
    def license_number(self):
        return self.__license_number

    # -------- CONSULTATION FEE (CONTROLLED) --------
    @property
    def consultation_fee(self):
        return self.__consultation_fee

    def set_consultation_fee(self, fee):
        if fee < 0:
            raise ValueError("Consultation fee cannot be negative")
        self.__consultation_fee = fee

    # -------- PATIENT MANAGEMENT --------
    def add_patient(self, patient_id):
        if patient_id not in self.__patients:
            self.__patients.append(patient_id)

    def remove_patient(self, patient_id):
        if patient_id in self.__patients:
            self.__patients.remove(patient_id)

    # -------- SERIALIZATION --------
    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "specialty": self.specialty,
            "license_number": self.__license_number,
            "consultation_fee": self.__consultation_fee,
            "patients": list(self.__patients)
        }
