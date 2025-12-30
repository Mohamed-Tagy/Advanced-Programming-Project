from controllers.base_controller import BaseController

class ReceptionistController(BaseController):

    def __init__(self, patient_controller,
                 doctor_controller,
                 appointment_controller):
        super().__init__()
        self.patient_controller = patient_controller
        self.doctor_controller = doctor_controller
        self.appointment_controller = appointment_controller

    def assign_patient_to_doctor(self, patient_id, doctor_id):
        patient = self.patient_controller.get(patient_id)
        doctor = self.doctor_controller.get(doctor_id)
        if not patient:
            raise ValueError("Patient not found")
        if not doctor:
            raise ValueError("Doctor not found")
        patient.assign_doctor(doctor_id)
        doctor.add_patient(patient_id)

        return "Patient assigned to doctor successfully"