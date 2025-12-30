from models.nurse import Nurse
from controllers.base_controller import BaseController

class NurseController(BaseController):
    def create_nurse(self, nurse_id, name, age, gender,
                     department, phone=None, email=None, address=None):
        if self.exists(nurse_id):
            raise ValueError("Nurse already exists")
        nurse = Nurse(
            nurse_id, name, age, gender, department,
            phone, email, address
        )
        self._items[nurse_id] = nurse
        return nurse

    def assign_patient(self, nurse_id, patient_id):
        nurse = self.get(nurse_id)
        if not nurse:
            raise ValueError("Nurse not found")
        nurse.assign_patient(patient_id)
