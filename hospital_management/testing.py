from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, person_id, name, age, gender, phone=None, email=None, address=None):
        self.__person_id = person_id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address

    @property
    def person_id(self):
        return self.__person_id

    def update_contact(self, phone=None, email=None, address=None):
        if phone is not None:
            self.phone = phone
        if email is not None:
            self.email = email
        if address is not None:
            self.address = address

    @abstractmethod
    def to_dict(self):
        pass

    def __str__(self):
        return f"{self.name} (ID: {self.__person_id})"


class Patient(Person):
    """Patient class for hospital management"""

    def __init__(self, patient_id, name, age, gender,
                 blood_type=None, allergies=None, medical_history=None,
                 phone=None, email=None, address=None):
        super().__init__(patient_id, name, age, gender, phone, email, address)

        self.blood_type = blood_type

        # ---- PRIVATE MEDICAL DATA ----
        self.__allergies = []
        self.__medical_history = []
        self.__medical_notes = []
        self.__admission_date = None
        self.__discharge_date = None
        self.__assigned_doctor = None

        if allergies is not None:
            if isinstance(allergies, str):
                self.__allergies.append(allergies)
            else:
                self.__allergies.extend(allergies)

        if medical_history is not None:
            if isinstance(medical_history, str):
                self.__medical_history.append(medical_history)
            else:
                self.__medical_history.extend(medical_history)


    def admit(self, admission_date, doctor_id):
        self.__admission_date = admission_date
        self.__assigned_doctor = doctor_id
        return f"{self.name} admitted on {admission_date} under doctor {doctor_id}"

    def discharge(self, discharge_date, doctor_id):
        self.__discharge_date = discharge_date
        self.__assigned_doctor = doctor_id
        return f"{self.name} discharged on {discharge_date} under doctor {doctor_id}"

    def add_allergy(self, allergy):
        if allergy not in self.__allergies:
            self.__allergies.append(allergy)
            return f"Allergy '{allergy}' added to {self.name}'s record"
        return f"Allergy '{allergy}' is already recorded"

    def add_to_medical_history(self, condition):
        if condition not in self.__medical_history:
            self.__medical_history.append(condition)
            return f"Added '{condition}' to {self.name}'s medical history"
        return f"'{condition}' already in medical history"

    def add_medical_note(self, note, doctor_name):
        self.__medical_notes.append({
            "Dr": doctor_name,
            "Note": note
        })
        return f"Note added by Dr. {doctor_name}"

    def get_medical_summary(self):
        status = "Admitted" if self.__admission_date else "Not admitted"
        return (
            f"Patient ID: {self.person_id}\n"
            f"Name: {self.name}\n"
            f"Blood Type: {self.blood_type if self.blood_type else 'Not recorded'}\n"
            f"Allergies: {', '.join(self.__allergies) if self.__allergies else 'None'}\n"
            f"Past Conditions: {', '.join(self.__medical_history) if self.__medical_history else 'None'}\n"
            f"Admission Status: {status}\n"
            f"Assigned Doctor: {self.__assigned_doctor if self.__assigned_doctor else 'None'}\n"
            f"Medical Notes: {len(self.__medical_notes)} note(s)"
        )

    def is_admitted(self):
        if self.__admission_date:
            return f"Patient {self.name} is currently admitted (since {self.__admission_date})"
        return f"Patient {self.name} is not admitted"


    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "blood_type": self.blood_type,
            "allergies": list(self.__allergies),
            "medical_history": list(self.__medical_history),
            "admitted": self.__admission_date is not None,
            "assigned_doctor": self.__assigned_doctor
        }

    def __str__(self):
        status = "Admitted" if self.__admission_date else "Not admitted"
        return f"Patient {self.name} (ID: {self.person_id}) - Status: {status}"

class PatientController:
    def __init__(self):
        self.patients = {}   # patient_id -> Patient object

    def create_patient(self, patient_id, name, age, gender,
                       blood_type=None, phone=None, email=None, address=None):
        if patient_id in self.patients:
            raise ValueError("Patient already exists")

        patient = Patient(
            patient_id, name, age, gender,
            blood_type, phone=phone, email=email, address=address
        )
        self.patients[patient_id] = patient
        return patient

    def admit_patient(self, patient_id, admission_date, doctor_id):
        patient = self.patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.admit(admission_date, doctor_id)

    def discharge_patient(self, patient_id, discharge_date, doctor_id):
        patient = self.patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient.discharge(discharge_date, doctor_id)

    def get_patient(self, patient_id):
        return self.patients.get(patient_id)


class Staff(Person):
    def __init__(self, staff_id, name, age, gender, role,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, phone, email, address)
        self.__role = role

    @property
    def role(self):
        return self.__role

    def update_role(self, new_role):
        self.__role = new_role

    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "role": self.__role
        }


class Doctor(Staff):
    def __init__(self, doctor_id, name, age, gender, specialty, license_number,
                 phone=None, email=None, address=None):
        super().__init__(doctor_id, name, age, gender, "Doctor", phone, email, address)

        self.specialty = specialty
        self.__license_number = license_number          # sensitive
        self.__patients = []
        self.__consultation_fee = 0                     # controlled

    # -------- LICENSE (READ-ONLY) --------
    @property
    def license_number(self):
        return self.__license_number

    # -------- CONSULTATION FEE (CONTROLLED) --------
    @property
    def consultation_fee(self):
        return self.__consultation_fee

    def set_consultation_fee(self, fee):
        if fee < 0:
            raise ValueError("Consultation fee cannot be negative")
        self.__consultation_fee = fee

    # -------- PATIENT MANAGEMENT --------
    def add_patient(self, patient_id):
        if patient_id not in self.__patients:
            self.__patients.append(patient_id)

    def remove_patient(self, patient_id):
        if patient_id in self.__patients:
            self.__patients.remove(patient_id)

    # -------- SERIALIZATION --------
    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "specialty": self.specialty,
            "license_number": self.__license_number,
            "consultation_fee": self.__consultation_fee,
            "patients": list(self.__patients)
        }


class Receptionist(Staff):
    def __init__(self, staff_id, name, age, gender,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, "Receptionist", phone, email, address)
        self.__registered_patients = []

    def register_patient(self, patient_id):
        self.__registered_patients.append(patient_id)

    def to_dict(self):
        return {
            "id": self.person_id,
            "registered_patients": self.__registered_patients
        }


class Technician(Staff):
    def __init__(self, staff_id, name, age, gender, specialty,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, "Technician", phone, email, address)
        self.specialty = specialty
        self.__tasks = []

    def assign_task(self, task):
        self.__tasks.append(task)

    def to_dict(self):
        return {
            "id": self.person_id,
            "specialty": self.specialty,
            "tasks": self.__tasks
        }

class Admin(Staff):
    def __init__(self, staff_id, name, age, gender,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, "Admin", phone, email, address)
        self.__permissions = []   # private (security-critical)

    def add_permission(self, permission):
        if permission not in self.__permissions:
            self.__permissions.append(permission)

    def remove_permission(self, permission):
        if permission in self.__permissions:
            self.__permissions.remove(permission)

    def has_permission(self, permission):
        return permission in self.__permissions

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "permissions": list(self.__permissions)  # safe copy
        })
        return data


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
    
    def __str__(self):
        return f"Appointment {self.appointment_id}: {self.patient_id} with Dr. {self.doctor_id} on {self.appointment_date}"


class Billing:
    """Billing class for hospital payments"""
    
    def __init__(self, bill_id, patient_id, patient_name, amount, service_description=""):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.amount = amount
        self.service_description = service_description
        self.payment_status = "Pending"  # Pending, Paid, Partially Paid, Overdue
        self.payment_date = None
        self.payment_method = ""
    
    def make_payment(self, amount_paid, payment_method="Cash", payment_date=""):
        """Record a payment"""
        if amount_paid <= 0:
            return "Payment amount must be positive"
        
        if amount_paid > self.amount:
            return f"Payment (${amount_paid}) exceeds bill amount (${self.amount})"
        
        self.amount -= amount_paid
        self.payment_method = payment_method
        
        if payment_date:
            self.payment_date = payment_date
        else:
            from datetime import datetime
            self.payment_date = datetime.now().strftime("%Y-%m-%d")
        
        if self.amount == 0:
            self.payment_status = "Fully Paid"
        else:
            self.payment_status = "Partially Paid"
        
        return (f"Payment of ${amount_paid} received from {self.patient_name}\n"
                f"Remaining balance: ${self.amount}\n"
                f"Status: {self.payment_status}")
    
    def add_charge(self, additional_amount, description=""):
        """Add additional charge to bill"""
        self.amount += additional_amount
        
        if description:
            self.service_description += f"; {description}"
        
        if self.payment_status == "Fully Paid":
            self.payment_status = "Pending"
        
        return f"Added ${additional_amount} charge. New total: ${self.amount}"
    
    def apply_discount(self, discount_percentage, reason=""):
        """Apply discount to bill"""
        if discount_percentage <= 0 or discount_percentage > 100:
            return "Discount percentage must be between 1-100"
        
        discount_amount = (self.amount * discount_percentage) / 100
        self.amount -= discount_amount
        
        discount_note = f" ({reason})" if reason else ""
        return f"Applied {discount_percentage}% discount{discount_note}. New total: ${self.amount:.2f}"
    
    def get_bill_summary(self):
        """Get billing summary"""
        return (f"Bill ID: {self.bill_id}\n"
                f"Patient: {self.patient_name} (ID: {self.patient_id})\n"
                f"Service: {self.service_description}\n"
                f"Amount Due: ${self.amount:.2f}\n"
                f"Status: {self.payment_status}\n"
                f"Payment Date: {self.payment_date if self.payment_date else 'Not paid yet'}\n"
                f"Payment Method: {self.payment_method if self.payment_method else 'Not specified'}")
    
    def is_paid(self):
        """Check if bill is fully paid"""
        if self.payment_status == "Fully Paid":
            return f"Bill {self.bill_id} is fully paid"
        else:
            return f"Bill {self.bill_id} has ${self.amount:.2f} remaining"
    
    def __str__(self):
        return f"Bill {self.bill_id}: {self.patient_name} - ${self.amount} ({self.payment_status})"

class HospitalController:
    def __init__(self, patient_controller, doctor_controller):
        self.patient_controller = patient_controller
        self.doctor_controller = doctor_controller

    def assign_patient_to_doctor(self, patient_id, doctor_id):
        patient = self.patient_controller.get_patient(patient_id)
        doctor = self.doctor_controller.get_doctor(doctor_id)

        if not patient or not doctor:
            raise ValueError("Invalid patient or doctor")

        doctor.add_patient(patient_id)
        patient.admit("Assigned", doctor_id)

class HospitalStatisticsController:
    def __init__(self,
                 doctor_controller,
                 nurse_controller,
                 admin_controller,
                 receptionist_controller,
                 technician_controller,
                 patient_controller,
                 appointment_controller,
                 billing_controller):

        self.doctors = doctor_controller
        self.nurses = nurse_controller
        self.admins = admin_controller
        self.receptionists = receptionist_controller
        self.technicians = technician_controller
        self.patients = patient_controller
        self.appointments = appointment_controller
        self.billing = billing_controller

    # ---------------- STAFF ----------------

    def total_staff_count(self):
        return (
            len(self.doctors.get_all()) +
            len(self.nurses.get_all()) +
            len(self.admins.get_all()) +
            len(self.receptionists.get_all()) +
            len(self.technicians.get_all())
        )

    def staff_by_role(self):
        return {
            "Doctors": len(self.doctors.get_all()),
            "Nurses": len(self.nurses.get_all()),
            "Admins": len(self.admins.get_all()),
            "Receptionists": len(self.receptionists.get_all()),
            "Technicians": len(self.technicians.get_all())
        }

    # ---------------- AVAILABILITY ----------------

    def available_doctors(self, max_patients=10):
        available = []
        for doctor in self.doctors.get_all():
            if len(doctor.to_dict()["patients"]) < max_patients:
                available.append(doctor)
        return available

    def available_nurses(self, max_patients=5):
        available = []
        for nurse in self.nurses.get_all():
            if len(nurse.to_dict()["assigned_patients"]) < max_patients:
                available.append(nurse)
        return available

    def availability_summary(self):
        return {
            "Available Doctors": len(self.available_doctors()),
            "Available Nurses": len(self.available_nurses())
        }

    # ---------------- PATIENTS ----------------

    def total_patients(self):
        return len(self.patients.get_all())

    def admitted_patients(self):
        return [
            p for p in self.patients.get_all()
            if p.is_admitted()
        ]

    # ---------------- APPOINTMENTS ----------------

    def appointment_summary(self):
        summary = {
            "Scheduled": 0,
            "Completed": 0,
            "Cancelled": 0,
            "No-show": 0
        }

        for appointment in self.appointments.get_all():
            status = appointment.status
            if status in summary:
                summary[status] += 1

        return summary

    # ---------------- BILLING ----------------

    def financial_summary(self):
        total_due = 0
        total_paid = 0

        for bill in self.billing.get_all():
            if bill.payment_status == "Fully Paid":
                total_paid += bill.amount
            else:
                total_due += bill.amount

        return {
            "Total Outstanding": total_due,
            "Total Collected": total_paid
        }

    # ---------------- MASTER SUMMARY ----------------

    def hospital_overview(self):
        return {
            "Total Staff": self.total_staff_count(),
            "Staff Breakdown": self.staff_by_role(),
            "Patients": self.total_patients(),
            "Admitted Patients": len(self.admitted_patients()),
            "Availability": self.availability_summary(),
            "Appointments": self.appointment_summary(),
            "Finance": self.financial_summary()
        }


class BaseController:
    def __init__(self):
        self._items = {}

    def exists(self, item_id):
        return item_id in self._items

    def get(self, item_id):
        return self._items.get(item_id)

    def get_all(self):
        return list(self._items.values())

    def remove(self, item_id):
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

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

class BillingController(BaseController):

    def create_bill(self, bill_id, patient_id, patient_name,
                    amount, description=""):
        if self.exists(bill_id):
            raise ValueError("Bill already exists")

        bill = Billing(bill_id, patient_id, patient_name, amount, description)
        self._items[bill_id] = bill
        return bill

    def make_payment(self, bill_id, amount, method="Cash", date=""):
        bill = self.get(bill_id)
        if not bill:
            raise ValueError("Bill not found")
        return bill.make_payment(amount, method, date)

    def add_charge(self, bill_id, amount, description=""):
        bill = self.get(bill_id)
        if not bill:
            raise ValueError("Bill not found")
        return bill.add_charge(amount, description)

    def apply_discount(self, bill_id, percentage, reason=""):
        bill = self.get(bill_id)
        if not bill:
            raise ValueError("Bill not found")
        return bill.apply_discount(percentage, reason)

class NurseController(BaseController):

    def create_nurse(self, nurse_id, name, age, gender,
                     department, phone=None, email=None, address=None):
        if self.exists(nurse_id):
            raise ValueError("Nurse already exists")

        nurse = Nurse(
            nurse_id, name, age, gender, department,
            phone, email, address
        )
        self._items[nurse_id] = nurse
        return nurse

    def assign_patient(self, nurse_id, patient_id):
        nurse = self.get(nurse_id)
        if not nurse:
            raise ValueError("Nurse not found")
        nurse.assign_patient(patient_id)
    
class DoctorController(BaseController):

    def create_doctor(self, doctor_id, name, age, gender,
                      specialty, license_number,
                      phone=None, email=None, address=None):
        if self.exists(doctor_id):
            raise ValueError("Doctor already exists")

        doctor = Doctor(
            doctor_id, name, age, gender, specialty,
            license_number, phone, email, address
        )
        self._items[doctor_id] = doctor
        return doctor

    def assign_patient(self, doctor_id, patient_id):
        doctor = self.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.add_patient(patient_id)

    def remove_patient(self, doctor_id, patient_id):
        doctor = self.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.remove_patient(patient_id)

    def set_fee(self, doctor_id, fee):
        doctor = self.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        doctor.set_consultation_fee(fee)

class AdminController(BaseController):

    def create_admin(self, admin_id, name, age, gender,
                     phone=None, email=None, address=None):
        if self.exists(admin_id):
            raise ValueError("Admin already exists")

        admin = Admin(
            admin_id, name, age, gender,
            phone, email, address
        )
        self._items[admin_id] = admin
        return admin

    def add_permission(self, admin_id, permission):
        admin = self.get(admin_id)
        if not admin:
            raise ValueError("Admin not found")
        admin.add_permission(permission)

class ReceptionistController:

    def __init__(self, patient_controller,
                 doctor_controller,
                 appointment_controller):
        self.patient_controller = patient_controller
        self.doctor_controller = doctor_controller
        self.appointment_controller = appointment_controller

    def assign_patient_to_doctor(self, patient_id, doctor_id):
        patient = self.patient_controller.get(patient_id)
        doctor = self.doctor_controller.get(doctor_id)

        if not patient or not doctor:
            raise ValueError("Patient or Doctor not found")

        patient.assign_doctor(doctor_id)
        doctor.add_patient(patient_id)

        return True


