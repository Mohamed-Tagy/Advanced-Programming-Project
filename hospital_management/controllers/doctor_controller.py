from hospital_management.models.doctor import Doctor
from hospital_management.controllers.base_controller import BaseController
from hospital_management.database.db_manager import Database

class DoctorController(BaseController):
    def __init__(self):
        super().__init__()
        self.db = Database()

    def create_doctor(self, doctor_id, name, age, gender, specialty, license_number,
                      phone=None, email=None, address=None):
        if self.exists(doctor_id):
            raise ValueError("Doctor already exists")

        doctor = Doctor(doctor_id, name, age, gender, specialty, license_number,
                        phone, email, address)
        self._items[doctor_id] = doctor

        self.db.execute(
            "INSERT INTO staff (staff_id, name, age, gender, role, specialty, license_number, department, permissions) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (doctor_id, name, age, gender, "Doctor", specialty, license_number, None, "")
        )
        return doctor

    def get_doctor(self, doctor_id):
        if doctor_id in self._items:
            return self._items[doctor_id]

        row = self.db.fetchone(
            "SELECT staff_id, name, age, gender, specialty, license_number FROM staff WHERE staff_id=? AND role='Doctor'",
            (doctor_id,)
        )
        if row:
            doctor = Doctor(row[0], row[1], row[2], row[3], row[4], row[5])
            self._items[doctor_id] = doctor
            return doctor
        return None

    def assign_patient(self, doctor_id, patient_id):
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        if not doctor.add_patient(patient_id):
            raise ValueError("Patient already assigned to this doctor")
        return True

    def remove_patient(self, doctor_id, patient_id):
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        if not doctor.remove_patient(patient_id):
            raise ValueError("Patient not assigned to this doctor")
        return True

    def set_fee(self, doctor_id, fee):
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.set_consultation_fee(fee)
        return True
