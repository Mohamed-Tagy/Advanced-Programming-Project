class Appointment:
    """Appointment class for scheduling patient visits"""
    
    def __init__(self, appointment_id, patient_id, doctor_id, date, time, 
                 reason="", status="Scheduled"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.reason = reason
        self.status = status  
        self.notes = ""
        self.outcome = None
        self.outcome_type = None
    
    def reschedule(self, new_date, new_time):
        """Reschedule the appointment"""
        old_date_time = f"{self.date} {self.time}"
        self.date = new_date
        self.time = new_time
        return f"Appointment {self.appointment_id} rescheduled from {old_date_time} to {new_date} {new_time}"
    
    def cancel(self):
        """Cancel the appointment"""
        if self.status == "Cancelled":
            return f"Appointment {self.appointment_id} is already cancelled"
        
        self.status = "Cancelled"
        return f"Appointment {self.appointment_id} on {self.date} at {self.time} has been cancelled"
    
    def mark_no_show(self):
        """Mark patient as did not show up for appointment"""
        if self.status == "No-show":
            return f"Appointment {self.appointment_id} already marked as no-show"
        
        self.status = "No-show"
        self.notes = "Patient did not show up for appointment"
        
        return (f"Appointment {self.appointment_id} marked as NO-SHOW\n"
                f"Patient {self.patient_id} failed to attend appointment with Dr. {self.doctor_id}\n"
                f"Date: {self.date} Time: {self.time}")

    def get_appointment_info(self):
        """Get appointment details"""
        return (f"Appointment ID: {self.appointment_id}\n"
                f"Patient ID: {self.patient_id}\n"
                f"Doctor ID: {self.doctor_id}\n"
                f"Date: {self.date}\n"
                f"Time: {self.time}\n"
                f"Reason: {self.reason}\n"
                f"Status: {self.status}\n"
                f"Notes: {self.notes if self.notes else 'No notes'}")

    def to_dict(self):
        """Return appointment as dict for easy printing / database insertion"""
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date,
            "time": self.time,
            "reason": self.reason,
            "status": self.status,
            "notes": self.notes,
            "outcome": self.outcome,
            "outcome_type": self.outcome_type
        }
    
    def __str__(self):
        return f"Appointment {self.appointment_id}: {self.patient_id} with Dr. {self.doctor_id} on {self.date}"