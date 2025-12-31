from backend.models.appointment import Appointment 
from backend.controllers.base_controller import BaseController 
from backend.database.db_manager import Database 

class AppointmentController(BaseController):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self._items = {} 


    def update_appointment_status(self, appointment_id, new_status):
        """Updates the status directly and refreshes the cache."""
        query = "UPDATE appointments SET status = ? WHERE appointment_id = ?"
        self.db.execute(query, (new_status, appointment_id))
        

        if appointment_id in self._items:
            self._items[appointment_id].status = new_status
        else:

            self.get_appointment(appointment_id)
            
        return True

    def exists(self, appointment_id):
        row = self.db.fetchone("SELECT 1 FROM appointments WHERE appointment_id=?", (appointment_id,))
        return row is not None

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

    def get_all(self):
        """Fetches all appointments and syncs with cache."""
        rows = self.db.fetchall(
            "SELECT appointment_id, patient_id, doctor_id, date, time, reason, status, notes, outcome, outcome_type "
            "FROM appointments"
        )
        appointments = []
        for row in rows:
            app = self._map_row_to_appointment(row)
            self._items[row[0]] = app
            appointments.append(app)
        return appointments

    def get_appointment(self, appointment_id):
        row = self.db.fetchone(
            "SELECT appointment_id, patient_id, doctor_id, date, time, reason, status, notes, outcome, outcome_type "
            "FROM appointments WHERE appointment_id=?",
            (appointment_id,)
        )
        if row:
            appointment = self._map_row_to_appointment(row)
            self._items[appointment_id] = appointment
            return appointment
        return None

    def _map_row_to_appointment(self, row):
        """Helper to create Appointment object from database row."""

        app = Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        app.notes = row[7]
        app.outcome = row[8]
        app.outcome_type = row[9]
        return app

    def update_appointment(self, appointment: Appointment):
        """Push local appointment object changes to DB"""
        self.db.execute(
            "UPDATE appointments SET date=?, time=?, reason=?, status=?, notes=?, outcome=?, outcome_type=? "
            "WHERE appointment_id=?",
            (appointment.appointment_date, appointment.appointment_time, appointment.reason,
             appointment.status, appointment.notes, appointment.outcome, appointment.outcome_type, appointment.appointment_id)
        )


    def get_by_patient(self, patient_id):
        rows = self.db.fetchall(
            "SELECT appointment_id, patient_id, doctor_id, date, time, reason, status, notes, outcome, outcome_type "
            "FROM appointments WHERE patient_id=?",
            (patient_id,)
        )
        return [self._map_row_to_appointment(row) for row in rows]

    def cancel(self, appointment_id):
        return self.update_appointment_status(appointment_id, "Cancelled")

    def complete(self, appointment_id, notes=""):
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")
        appointment.complete(notes)
        self.update_appointment(appointment)
        return True