from models.doctor import Doctor
from controllers.base_controller import BaseController

class DoctorController(BaseController):

    def create_doctor(self, doctor_id, name, age, gender,
                      specialty, license_number,
                      phone=None, email=None, address=None):
        if self.exists(doctor_id):
            raise ValueError("Doctor already exists")

        doctor = Doctor(
            doctor_id, name, age, gender, specialty,
            license_number, phone, email, address
        )
        self._items[doctor_id] = doctor
        return doctor

    def assign_patient(self, doctor_id, patient_id):
        doctor = self.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.add_patient(patient_id)

    def remove_patient(self, doctor_id, patient_id):
        doctor = self.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.remove_patient(patient_id)

    def set_fee(self, doctor_id, fee):
        doctor = self.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.set_consultation_fee(fee)
