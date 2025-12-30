from models.appointment import Appointment
from controllers.base_controller import BaseController

class AppointmentController(BaseController):

    def create_appointment(self, appointment_id, patient_id, doctor_id,
                           date, time, reason=""):
        if self.exists(appointment_id):
            raise ValueError("Appointment already exists")

        appointment = Appointment(
            appointment_id, patient_id, doctor_id, date, time, reason
        )
        self._items[appointment_id] = appointment
        return appointment

    def reschedule(self, appointment_id, new_date, new_time):
        appointment = self.get(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        return appointment.reschedule(new_date, new_time)

    def cancel(self, appointment_id):
        appointment = self.get(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        return appointment.cancel()

    def complete(self, appointment_id, notes=""):
        appointment = self.get(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        return appointment.complete(notes)

    def set_outcome(self, appointment_id, outcome_type, details=""):
        appointment = self.get(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        return appointment.set_outcome(outcome_type, details)
