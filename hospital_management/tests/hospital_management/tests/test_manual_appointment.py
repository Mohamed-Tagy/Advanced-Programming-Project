import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from hospital_management.controllers.appointment_controller import AppointmentController


def main():
    controller = AppointmentController()

    # 1️⃣ Create an appointment
    appointment = controller.create_appointment(
        appointment_id="A100",
        patient_id="P100",
        doctor_id="D001",
        date="2026-01-05",
        time="10:00",
        reason="Routine Checkup"
    )
    assert appointment is not None
    print("Created appointment:", appointment.to_dict())

    # 2️⃣ Reschedule the appointment
    controller.reschedule("A100", "2026-01-06", "11:00")
    appointment = controller.get_appointment("A100")
    print("After reschedule:", appointment.to_dict())

    # 3️⃣ Complete the appointment
    controller.complete("A100", notes="Patient healthy, no issues")
    appointment = controller.get_appointment("A100")
    print("After completion:", appointment.to_dict())

    # 4️⃣ Set an outcome
    controller.set_outcome("A100", outcome_type=1)
    appointment = controller.get_appointment("A100")
    print("After setting outcome:", appointment.to_dict())

    # 5️⃣ Cancel (just to see DB update, normally wouldn't cancel completed)
    controller.cancel("A100")
    appointment = controller.get_appointment("A100")
    print("After cancel attempt:", appointment.to_dict())


if __name__ == "__main__":
    main()
