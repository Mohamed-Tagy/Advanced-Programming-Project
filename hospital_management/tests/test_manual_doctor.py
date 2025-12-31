import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hospital_management.controllers.doctor_controller import DoctorController



def main():
    controller = DoctorController()

    doctor = controller.create_doctor(
        doctor_id="D001",
        name="Dr. House",
        age=45,
        gender="M",
        specialty="Diagnostics",
        license_number="LIC123"
    )
    print("Created doctor:", doctor.to_dict())

    controller.assign_patient("D001", "P100")
    controller.assign_patient("D001", "P101")
    doctor = controller.get_doctor("D001")
    print("After assigning patients:", doctor.to_dict())

    try:
        controller.assign_patient("D001", "P100")
    except ValueError as e:
        print("Duplicate assignment attempt:", e)

    controller.remove_patient("D001", "P101")
    doctor = controller.get_doctor("D001")
    print("After removing patient:", doctor.to_dict())

    controller.set_fee("D001", 150)
    doctor = controller.get_doctor("D001")
    print("After setting fee:", doctor.to_dict())

if __name__ == "__main__":
    main()
