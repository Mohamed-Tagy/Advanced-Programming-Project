from hospital_management.models.appointment import Appointment
from hospital_management.controllers.base_controller import BaseController
from hospital_management.database.db_manager import Database

class AppointmentController(BaseController):
    def __init__(self):
        super().__init__()
        self.db = Database()

    def create_appointment(self, appointment_id, patient_id, doctor_id,
                           date, time, reason=""):
        if self.exists(appointment_id):
            raise ValueError("Appointment already exists")

        appointment = Appointment(appointment_id, patient_id, doctor_id, date, time, reason)
        self._items[appointment_id] = appointment
        self.db.execute(
            "INSERT INTO appointments (appointment_id, patient_id, doctor_id, date, time, reason, status, notes, outcome, outcome_type) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (appointment_id, patient_id, doctor_id, date, time, reason, appointment.status,
             appointment.notes, appointment.outcome, appointment.outcome_type)
        )
        return appointment

    def get_appointment(self, appointment_id):
        if appointment_id in self._items:
            return self._items[appointment_id]

        row = self.db.fetchone(
            "SELECT appointment_id, patient_id, doctor_id, date, time, reason, status, notes, outcome, outcome_type "
            "FROM appointments WHERE appointment_id=?",
            (appointment_id,)
        )
        if row:
            appointment = Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            appointment.notes = row[7]
            appointment.outcome = row[8]
            appointment.outcome_type = row[9]
            self._items[appointment_id] = appointment
            return appointment
        return None

    def update_appointment(self, appointment: Appointment):
        """Push local appointment object changes to DB"""
        self.db.execute(
            "UPDATE appointments SET date=?, time=?, reason=?, status=?, notes=?, outcome=?, outcome_type=? "
            "WHERE appointment_id=?",
            (appointment.appointment_date, appointment.appointment_time, appointment.reason,
             appointment.status, appointment.notes, appointment.outcome, appointment.outcome_type, appointment.appointment_id)
        )

    # Wrap Appointment methods and sync DB
    def reschedule(self, appointment_id, new_date, new_time):
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        result = appointment.reschedule(new_date, new_time)
        self.update_appointment(appointment)
        return result

    def cancel(self, appointment_id):
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        result = appointment.cancel()
        self.update_appointment(appointment)
        return result

    def complete(self, appointment_id, notes=""):
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        result = appointment.complete(notes)
        self.update_appointment(appointment)
        return result

    def set_outcome(self, appointment_id, outcome_type, details=""):
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        result = appointment.set_outcome(outcome_type, details)
        self.update_appointment(appointment)
        return result
