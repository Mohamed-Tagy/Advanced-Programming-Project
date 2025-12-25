class Doctor:
    """Doctor class for the hospital management system"""
    
    def __init__(self, doctor_id, name, specialty, license_number):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty  # e.g., "Cardiology", "Pediatrics"
        self.license_number = license_number
        self.patients = []  # List of patient IDs assigned to this doctor
        self.appointments = []  # List of appointment IDs
    
    def add_patient(self, patient_id, patient_name, condition_code):
        """Add a patient to doctor's care list with their medical condition"""
        
        # Common medical condition codes (expand as needed)
        condition_codes = {
            'BLACK': 'Critical/Emergency',
            'RED': 'Immediate/Life-threatening', 
            'YELLOW': 'Urgent',
            'GREEN': 'Minor/Non-urgent',
            'WHITE': 'Discharged/Non-acute'
        }
        
        if patient_id in self.patients:
            return f"Patient {patient_name} (ID: {patient_id}) is already registered"
        else:
            self.patients.append(patient_id)
            condition_desc = condition_codes.get(condition_code.upper(), 'Unknown condition')
            return f"Patient {patient_name} (ID: {patient_id}) with condition {condition_code} ({condition_desc}) has been registered"

    def remove_patient(self, patient_id, patient_name):
        """Remove a patient from doctor's care list"""
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            return f"Patient {patient_name} (ID: {patient_id}) has been removed"
        else:
            return f"Patient {patient_name} (ID: {patient_id}) is not registered with this doctor"
    
    def schedule_appointment(self, appointment_id, appointment_date):
        """Schedule a new appointment with date checking"""
        
        # Single loop checking both conditions
        for existing_id, existing_date in self.appointments:
            if existing_id == appointment_id:
                return f"Appointment ID {appointment_id} already exists"
            if existing_date == appointment_date:
                return f"Date {appointment_date} is already booked with appointment {existing_id}"
        
        # Schedule the appointment
        self.appointments.append((appointment_id, appointment_date))
        return f"Appointment ID {appointment_id} scheduled for {appointment_date}"
    
    def cancel_appointment(self, appointment_id):
        """Cancel an existing appointment"""
        for i, (app_id, date) in enumerate(self.appointments):
            if app_id == appointment_id:
                self.appointments.pop(i)
                return f"Appointment ID {appointment_id} scheduled for {date} has been cancelled"
        return f"Appointment ID {appointment_id} not found in schedule"
    
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