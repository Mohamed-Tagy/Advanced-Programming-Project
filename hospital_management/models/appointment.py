class Appointment:

    VALID_STATUSES = {"Scheduled", "Completed", "Cancelled", "No-show"}

    def __init__(self, appointment_id, patient_id, doctor_id,
                 appointment_date, appointment_time, reason=""):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id

        self.__date = appointment_date
        self.__time = appointment_time
        self.__reason = reason

        self.__status = "Scheduled"
        self.__notes = ""
        self.__outcome = None
        self.__outcome_type = None

    @property
    def status(self):
        return self.__status

    @property
    def date(self):
        return self.__date

    @property
    def time(self):
        return self.__time

    def reschedule(self, new_date, new_time):
        if self.__status in {"Cancelled", "Completed"}:
            raise ValueError("Cannot reschedule a finished appointment")

        self.__date = new_date
        self.__time = new_time

    def cancel(self):
        if self.__status == "Cancelled":
            raise ValueError("Appointment already cancelled")
        self.__status = "Cancelled"

    def mark_no_show(self):
        if self.__status != "Scheduled":
            raise ValueError("Only scheduled appointments can be no-show")
        self.__status = "No-show"
        self.__notes = "Patient did not attend"

    def complete(self, notes=""):
        if self.__status != "Scheduled":
            raise ValueError("Only scheduled appointments can be completed")
        self.__status = "Completed"
        self.__notes = notes

    def set_outcome(self, outcome_type, details=""):
        outcomes = {
            1: "Healthy – no action required",
            2: "Follow-up and medication required",
            3: "Hospital admission required",
            4: "Surgery required",
            5: f"Other: {details}" if details else "Other condition"
        }

        if outcome_type not in outcomes:
            raise ValueError("Invalid outcome type")

        self.__outcome_type = outcome_type
        self.__outcome = outcomes[outcome_type]

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.__date,
            "time": self.__time,
            "reason": self.__reason,
            "status": self.__status,
            "notes": self.__notes,
            "outcome": self.__outcome,
            "outcome_type": self.__outcome_type
        }

    def __str__(self):
        return (
            f"Appointment {self.appointment_id} | "
            f"Patient {self.patient_id} → Doctor {self.doctor_id} | "
            f"{self.__date} {self.__time} | {self.__status}"
        )
