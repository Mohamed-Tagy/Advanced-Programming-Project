from models.doctor import Doctor

class DoctorController:
    def __init__(self):
        self.doctors = []

    def add_doctor(self, doctor: Doctor):
        self.doctors.append(doctor)

    def get_all_doctors(self):
        return self.doctors
