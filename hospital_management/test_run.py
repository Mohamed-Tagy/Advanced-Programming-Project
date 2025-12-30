from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.appointment_controller import AppointmentController
from controllers.billing_controller import BillingController

print('Initializing controllers...')

patient_ctrl = PatientController()
doctor_ctrl = DoctorController()
appointment_ctrl = AppointmentController()
billing_ctrl = BillingController()

print('Controllers initialized successfully!')
