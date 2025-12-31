from backend.models.patient import Patient
from backend.controllers.base_controller import BaseController 

class PatientController(BaseController):
    def __init__(self):
        super().__init__()



    def admit_patient(self, patient_id, admission_date=None, doctor_id=None):
        """Updates patient status to Admitted (1)."""
        if not self.exists(patient_id):
            raise ValueError("Patient not found")
        

        query = "UPDATE patients SET admitted = 1 WHERE patient_id = ?"
        success = self.execute_non_query(query, (patient_id,))
        
        if not success:
            raise Exception("Failed to admit patient in database")
        return True

    def discharge_patient(self, patient_id, discharge_date=None):
        """Updates patient status to Discharged (0)."""
        if not self.exists(patient_id):
            raise ValueError("Patient not found")
        
        query = "UPDATE patients SET admitted = 0 WHERE patient_id = ?"
        success = self.execute_non_query(query, (patient_id,))
        
        if not success:
            raise Exception("Failed to discharge patient in database")
        return True

    def add_medical_note(self, patient_id, note):
        """Adds a clinical note to the medical history."""
        return self.add_medical_history(patient_id, note)


    def _map_row_to_patient(self, row):
        """Converts database rows to Patient objects, including the admitted status."""
        patient = Patient(
            patient_id=row[0],
            name=row[1],
            age=row[2],
            gender=row[3],
            blood_type=row[4],
            phone=row[5],
            email=row[6],
            address=row[7],
            allergies=row[8].split(",") if row[8] else [],
            medical_history=row[9].split(",") if row[9] else []
        )


        if len(row) > 10:
            patient.admitted = row[10] 
        else:
            patient.admitted = 0
            
        return patient



    def update_patient(self, patient_id, name, email, phone):
        if not self.exists(patient_id):
            raise ValueError("Patient not found")

        query = "UPDATE patients SET name = ?, email = ?, phone = ? WHERE patient_id = ?"
        return self.execute_non_query(query, (name, email, phone, patient_id))

    def exists(self, patient_id):
        query = "SELECT 1 FROM patients WHERE patient_id = ?"
        result = self.execute_query(query, (patient_id,))
        return len(result) > 0

    def create_patient(self, patient_id, name, age, gender, **kwargs):
        if self.exists(patient_id):
            raise ValueError("Patient already exists")


        query = """
            INSERT INTO patients (
                patient_id, name, age, gender, admitted
            ) VALUES (?, ?, ?, ?, 0)
        """
        params = (patient_id, name, age, gender)
        return self.execute_non_query(query, params)

    def get_all(self):
        query = "SELECT * FROM patients"
        rows = self.execute_query(query)
        return [self._map_row_to_patient(row) for row in rows]

    def get_patient(self, patient_id):
        query = "SELECT * FROM patients WHERE patient_id=?"
        rows = self.execute_query(query, (patient_id,))
        return self._map_row_to_patient(rows[0]) if rows else None

    def add_medical_history(self, patient_id, condition):
        patient = self.get_patient(patient_id)
        if not patient: raise ValueError("Patient not found")
        
        patient.add_to_medical_history(condition)
        query = "UPDATE patients SET medical_history = ? WHERE patient_id = ?"
        updated_history = ",".join(patient.medical_history)
        return self.execute_non_query(query, (updated_history, patient_id))