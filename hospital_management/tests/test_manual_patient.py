import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from hospital_management.controllers.patient_controller import PatientController


def main():
    controller = PatientController()

    patient = controller.create_patient(
        patient_id="P100",
        name="Test User",
        age=40,
        gender="M",
        blood_type="O+"
    )
    assert patient is not None
    print("Created patient:", patient.to_dict())

    controller.admit_patient("P100", "2025-12-31", "D001")
    patient = controller.get_patient("P100")
    assert patient is not None
    print("After admission:", patient.to_dict())

    controller.add_allergy("P100", "Dust")
    controller.add_medical_history("P100", "Hypertension")
    patient = controller.get_patient("P100")
    assert patient is not None
    print("After adding allergy/history:", patient.to_dict())

    controller.discharge_patient("P100", "2026-01-02", "D001")
    patient = controller.get_patient("P100")
    assert patient is not None
    print("After discharge:", patient.to_dict())

if __name__ == "__main__":
    main()
