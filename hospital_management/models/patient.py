from models import Person

class Patient(Person):

    def __init__(self, patient_id, name, age, gender,
                 blood_type=None, allergies=None, medical_history=None,
                 phone=None, email=None, address=None):
        super().__init__(patient_id, name, age, gender, phone, email, address)

        self.blood_type = blood_type

        # ---- PRIVATE MEDICAL DATA ----
        self.__allergies = []
        self.__medical_history = []
        self.__medical_notes = []
        self.__admission_date = None
        self.__discharge_date = None
        self.__assigned_doctor = None

        # ---- INITIAL DATA HANDLING (YOUR LOGIC PRESERVED) ----
        if allergies is not None:
            if isinstance(allergies, str):
                self.__allergies.append(allergies)
            else:
                self.__allergies.extend(allergies)

        if medical_history is not None:
            if isinstance(medical_history, str):
                self.__medical_history.append(medical_history)
            else:
                self.__medical_history.extend(medical_history)

    # ----------------- YOUR METHODS (UNCHANGED LOGIC) -----------------

    def admit(self, admission_date, doctor_id):
        self.__admission_date = admission_date
        self.__assigned_doctor = doctor_id
        return f"{self.name} admitted on {admission_date} under doctor {doctor_id}"

    def discharge(self, discharge_date, doctor_id):
        self.__discharge_date = discharge_date
        self.__assigned_doctor = doctor_id
        return f"{self.name} discharged on {discharge_date} under doctor {doctor_id}"

    def add_allergy(self, allergy):
        if allergy not in self.__allergies:
            self.__allergies.append(allergy)
            return f"Allergy '{allergy}' added to {self.name}'s record"
        return f"Allergy '{allergy}' is already recorded"

    def add_to_medical_history(self, condition):
        if condition not in self.__medical_history:
            self.__medical_history.append(condition)
            return f"Added '{condition}' to {self.name}'s medical history"
        return f"'{condition}' already in medical history"

    def add_medical_note(self, note, doctor_name):
        self.__medical_notes.append({
            "Dr": doctor_name,
            "Note": note
        })
        return f"Note added by Dr. {doctor_name}"

    def get_medical_summary(self):
        status = "Admitted" if self.__admission_date else "Not admitted"
        return (
            f"Patient ID: {self.person_id}\n"
            f"Name: {self.name}\n"
            f"Blood Type: {self.blood_type if self.blood_type else 'Not recorded'}\n"
            f"Allergies: {', '.join(self.__allergies) if self.__allergies else 'None'}\n"
            f"Past Conditions: {', '.join(self.__medical_history) if self.__medical_history else 'None'}\n"
            f"Admission Status: {status}\n"
            f"Assigned Doctor: {self.__assigned_doctor if self.__assigned_doctor else 'None'}\n"
            f"Medical Notes: {len(self.__medical_notes)} note(s)"
        )

    def is_admitted(self):
        if self.__admission_date:
            return f"Patient {self.name} is currently admitted (since {self.__admission_date})"
        return f"Patient {self.name} is not admitted"

    # ----------------- REQUIRED BY PERSON -----------------

    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "blood_type": self.blood_type,
            "allergies": list(self.__allergies),
            "medical_history": list(self.__medical_history),
            "admitted": self.__admission_date is not None,
            "assigned_doctor": self.__assigned_doctor
        }

    def __str__(self):
        status = "Admitted" if self.__admission_date else "Not admitted"
        return f"Patient {self.name} (ID: {self.person_id}) - Status: {status}"