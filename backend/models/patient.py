from backend.models.person import Person

class Patient(Person):
    def __init__(self, patient_id, name, age, gender,
                 blood_type, allergies=None, medical_history=None,
                 phone=None, email=None, address=None):
        super().__init__(patient_id, name, age, gender, phone, email, address)

        self.blood_type = blood_type
        self.__allergies = []
        self.__medical_history = []
        self.__medical_notes = []
        self.__admission_date = None
        self.__discharge_date = None
        self.__assigned_doctor = None

        if allergies:
            self.__allergies.extend(allergies if isinstance(allergies, list) else [allergies])

        if medical_history:
            self.__medical_history.extend(medical_history if isinstance(medical_history, list) else [medical_history])

    def admit(self, admission_date, doctor_id):
        if self.is_admitted():
            raise ValueError("Patient is already admitted")
        self.__admission_date = admission_date
        self.__discharge_date = None
        self.__assigned_doctor = doctor_id
        return True

    def discharge(self, discharge_date, doctor_id):
        if not self.is_admitted():
            raise ValueError("Patient is not currently admitted")
        self.__discharge_date = discharge_date
        self.__assigned_doctor = doctor_id
        return True

    def add_allergy(self, allergy):
        if allergy not in self.__allergies:
            self.__allergies.append(allergy)

    def add_to_medical_history(self, condition):
        if condition not in self.__medical_history:
            self.__medical_history.append(condition)

    def add_medical_note(self, note, doctor_name):
        self.__medical_notes.append({"doctor": doctor_name, "note": note})

    def is_admitted(self):
        return self.__admission_date is not None and self.__discharge_date is None

    def to_dict(self) -> dict:
        base_dict = super().to_dict() 
        base_dict.update({
            "blood_type": self.blood_type,
            "allergies": list(self.__allergies),
            "medical_history": list(self.__medical_history),
            "medical_notes": list(self.__medical_notes),
            "admitted": self.is_admitted(),
            "admission_date": self.__admission_date,
            "discharge_date": self.__discharge_date,
            "assigned_doctor": self.__assigned_doctor
        })
        return base_dict
