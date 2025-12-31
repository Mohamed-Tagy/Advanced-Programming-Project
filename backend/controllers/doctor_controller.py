from backend.models.doctor import Doctor
from backend.database.db_manager import Database

class DoctorController:
    def __init__(self):
        self.db = Database()
        self._items = {}

    def exists(self, doctor_id):
        return doctor_id in self._items or \
               self.db.fetchone("SELECT 1 FROM staff WHERE staff_id=? AND role='Doctor'", (doctor_id,)) is not None

    def create_doctor(self, doctor_id, name, age, gender, specialty, license_number,
                      phone=None, email=None, address=None):
        if self.exists(doctor_id):
            raise ValueError("Doctor already exists")

        doctor = Doctor(doctor_id, name, age, gender, specialty, license_number, phone, email, address)

        self.db.execute(
            "INSERT INTO staff (staff_id, name, age, gender, role, specialty, license_number, department, permissions, status, fee) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (doctor_id, name, age, gender, "Doctor", specialty, license_number, None, "", "Admitted", doctor.consultation_fee)
        )

        self._items[doctor.person_id] = doctor
        return doctor

    def get_all(self):
        """Fetch all doctors from DB including status and fee."""
        rows = self.db.fetchall(
            "SELECT staff_id, name, age, gender, specialty, license_number, status, fee "
            "FROM staff WHERE role='Doctor'"
        )
        doctors = []
        for row in rows:
            doc = Doctor(row[0], row[1], row[2], row[3], row[4], row[5])
            # attach status and fee
            doc.status = row[6] if len(row) > 6 else "Admitted"
            doc.set_consultation_fee(row[7] if len(row) > 7 else 0.0)
            self._items[doc.person_id] = doc
            doctors.append(doc)
        return doctors

    def get_doctor(self, doctor_id):
        """Get a single doctor by ID."""
        if doctor_id in self._items:
            return self._items[doctor_id]

        row = self.db.fetchone(
            "SELECT staff_id, name, age, gender, specialty, license_number, status, fee "
            "FROM staff WHERE staff_id=? AND role='Doctor'",
            (doctor_id,)
        )
        if not row:
            return None

        doc = Doctor(row[0], row[1], row[2], row[3], row[4], row[5])
        doc.status = row[6] if len(row) > 6 else "Admitted"
        doc.set_consultation_fee(row[7] if len(row) > 7 else 0.0)
        self._items[doctor_id] = doc
        return doc

    def update_status(self, doctor_id, new_status):
        """Update status in DB and local cache."""
        self.db.execute(
            "UPDATE staff SET status=? WHERE staff_id=? AND role='Doctor'", 
            (new_status, doctor_id)
        )
        if doctor_id in self._items:
            self._items[doctor_id].status = new_status
        return True

    def set_fee(self, doctor_id, fee):
        """Update consultation fee in DB and Doctor object."""
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.set_consultation_fee(fee)
        self.db.execute("UPDATE staff SET fee=? WHERE staff_id=?", (fee, doctor_id))
        return True

    def assign_patient(self, doctor_id, patient_id):
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        if not doctor.add_patient(patient_id):
            raise ValueError("Patient already assigned")
        return True

    def remove_patient(self, doctor_id, patient_id):
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        if not doctor.remove_patient(patient_id):
            raise ValueError("Patient not assigned")
        return True
