# backend/controllers/auth_controller.py
import datetime

class AuthController:
    def __init__(self, patient_ctrl, admin_ctrl):
        self.patient_ctrl = patient_ctrl
        self.admin_ctrl = admin_ctrl

    def login(self, user_id, password):
        """Logic to identify user type and verify credentials"""

        admin = self.admin_ctrl.get_admin(user_id)
        if admin:

            return {"user": admin, "role": "admin", "route": "/admin-dashboard"}


        patient = self.patient_ctrl.get_patient(user_id)
        if patient:
            return {"user": patient, "role": "user", "route": "/user-dashboard"}
        
        return None

    def register_patient(self, data):
        """Logic for calculating age and creating the Patient record"""
        if self.patient_ctrl.exists(data['user_id']):
            raise ValueError(f"User ID '{data['user_id']}' already exists")


        today = datetime.date.today()
        dob = data['dob']
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


        return self.patient_ctrl.create_patient(
            patient_id=data['user_id'],
            name=data['full_name'],
            age=age,
            gender=data['gender'],
            phone=data['phone'],
            email=data['email'],
            blood_type="Not Specified"
        )


    def register_admin(self, data):
        """Logic for creating an Admin record"""

        if self.admin_ctrl.get_admin(data['user_id']):
            raise ValueError(f"Admin ID '{data['user_id']}' already exists")


        return self.admin_ctrl.create_admin(
            admin_id=data['user_id'],
            name=data['full_name'],
            email=data.get('email'),
            phone=data.get('phone')
        )