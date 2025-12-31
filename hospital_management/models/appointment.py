class Appointment:
    """Appointment class for scheduling patient visits"""
    
    def __init__(self, appointment_id, patient_id, doctor_id, appointment_date, appointment_time, 
                 reason="", status="Scheduled"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status  # Scheduled, Completed, Cancelled, No-show
        self.notes = ""
        self.outcome = None
        self.outcome_type = None
    
    def reschedule(self, new_date, new_time):
        """Reschedule the appointment"""
        old_date_time = f"{self.appointment_date} {self.appointment_time}"
        self.appointment_date = new_date
        self.appointment_time = new_time
        return f"Appointment {self.appointment_id} rescheduled from {old_date_time} to {new_date} {new_time}"
    
    def cancel(self):
        """Cancel the appointment"""
        if self.status == "Cancelled":
            return f"Appointment {self.appointment_id} is already cancelled"
        
        self.status = "Cancelled"
        return f"Appointment {self.appointment_id} on {self.appointment_date} at {self.appointment_time} has been cancelled"
    
    def mark_no_show(self):
        """Mark patient as did not show up for appointment"""
        if self.status == "No-show":
            return f"Appointment {self.appointment_id} already marked as no-show"
        
        self.status = "No-show"
        self.notes = "Patient did not show up for appointment"
        
        # Record in patient's history (if connected to patient object)
        return (f"Appointment {self.appointment_id} marked as NO-SHOW\n"
                f"Patient {self.patient_id} failed to attend appointment with Dr. {self.doctor_id}\n"
                f"Date: {self.appointment_date} Time: {self.appointment_time}")
    
    def set_outcome(self, outcome_type, details=""):
        """Set appointment outcome with medical conclusions"""
        
        outcomes = {
            1: "Patient is healthy, no further action needed",
            2: "Patient needs follow-up checkup and medication",
            3: "Patient requires hospital admission",
            4: "Patient requires surgery - schedule needed",
            5: f"Other: {details}" if details else "Other condition"
        }
        
        if outcome_type not in outcomes:
            return f"Invalid outcome type. Choose 1-5"
        
        self.outcome = outcomes[outcome_type]
        self.outcome_type = outcome_type
        
        # Auto actions based on outcome
        actions = {
            1: "Discharge with clean bill of health",
            2: "Prescribe medication and schedule follow-up",
            3: "Initiate hospital admission process",
            4: "Contact surgery scheduling department",
            5: f"Special case: {details}"
        }
        
        recommended_action = actions[outcome_type]
        
        return (f"Appointment {self.appointment_id} outcome set:\n"
                f"Conclusion: {self.outcome}\n"
                f"Recommended action: {recommended_action}")
    
    def get_outcome_summary(self):
        """Get outcome details if set"""
        if hasattr(self, 'outcome'):
            return (f"Appointment Outcome:\n"
                    f"- Conclusion: {self.outcome}\n"
                    f"- Type: {self.outcome_type}\n"
                    f"- Notes: {self.notes}")
        else:
            return "No outcome recorded for this appointment"
    
    def complete(self, notes=""):
        """Mark appointment as completed"""
        if self.status == "Completed":
            return f"Appointment {self.appointment_id} is already marked completed"
        
        self.status = "Completed"
        self.notes = notes
        return f"Appointment {self.appointment_id} marked as completed. Notes: {notes}"
    
    def get_appointment_info(self):
        """Get appointment details"""
        return (f"Appointment ID: {self.appointment_id}\n"
                f"Patient ID: {self.patient_id}\n"
                f"Doctor ID: {self.doctor_id}\n"
                f"Date: {self.appointment_date}\n"
                f"Time: {self.appointment_time}\n"
                f"Reason: {self.reason}\n"
                f"Status: {self.status}\n"
                f"Notes: {self.notes if self.notes else 'No notes'}")
    def to_dict(self):
        """Return appointment as dict for easy printing / database insertion"""
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.appointment_date,
            "time": self.appointment_time,
            "reason": self.reason,
            "status": self.status,
            "notes": self.notes,
            "outcome": self.outcome,
            "outcome_type": self.outcome_type
        }
    
    def __str__(self):
        return f"Appointment {self.appointment_id}: {self.patient_id} with Dr. {self.doctor_id} on {self.appointment_date}"
