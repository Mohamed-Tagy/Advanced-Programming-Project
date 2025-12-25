class Doctor:
    """Doctor class for the hospital management system"""
    
    def __init__(self, doctor_id, name, specialty, license_number):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty  # e.g., "Cardiology", "Pediatrics"
        self.license_number = license_number
        self.patients = []  # List of patient IDs assigned to this doctor
        self.appointments = []  # List of appointment IDs
    
    def add_patient(self, patient_id):
        """Add a patient to doctor's care list"""
        if patient_id not in self.patients:
            self.patients.append(patient_id)
            return True
        return False
    
    def remove_patient(self, patient_id):
        """Remove a patient from doctor's care list"""
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            return True
        return False
    
    def schedule_appointment(self, appointment_id):
        """Schedule a new appointment"""
        self.appointments.append(appointment_id)
    
    def cancel_appointment(self, appointment_id):
        """Cancel an existing appointment"""
        if appointment_id in self.appointments:
            self.appointments.remove(appointment_id)
            return True
        return False
    
    def get_patient_count(self):
        """Get number of patients under doctor's care"""
        return len(self.patients)
    
    def get_appointment_count(self):
        """Get number of scheduled appointments"""
        return len(self.appointments)
    
    def get_info(self):
        """Return doctor information as dictionary"""
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'specialty': self.specialty,
            'license_number': self.license_number,
            'patients': self.patients,
            'appointments': self.appointments
        }
    
    def __str__(self):
        return f"Dr. {self.name} ({self.specialty}) - License: {self.license_number}"