from models.appointment import Appointment

class AppointmentController:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, appointment: Appointment):
        self.appointments.append(appointment)

    def get_all_appointments(self):
        return self.appointments
