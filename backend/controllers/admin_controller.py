from backend.models.admin import Admin
from backend.controllers.base_controller import BaseController 
import datetime

class AdminController(BaseController):
    def __init__(self):
        super().__init__()

    def exists(self, admin_id):
        """Checks if an admin ID exists in the database."""
        query = "SELECT 1 FROM staff WHERE staff_id = ? AND role = 'Admin'"
        result = self.execute_query(query, (admin_id,))
        return len(result) > 0

    def create_admin(self, admin_id, name, dob=None, gender="Not Specified", 
                     phone=None, email=None, address=None):
        """Creates an admin in the database using the thread-safe pattern."""
        if self.exists(admin_id):
            raise ValueError(f"Admin with ID '{admin_id}' already exists")


        age = 0
        if dob:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


        admin = Admin(admin_id, name, age, gender, phone, email, address)


        query = """
            INSERT INTO staff (staff_id, name, age, gender, role, permissions) 
            VALUES (?, ?, ?, ?, ?, ?)
        """

        params = (admin_id, name, age, gender, "Admin", "")
        
        success = self.execute_non_query(query, params)
        if not success:
            raise Exception("Failed to insert admin into database")
            
        return admin

    def get_admin(self, admin_id):
        """Fetches a single admin's data for login or profile viewing."""
        query = "SELECT staff_id, name, age, gender, permissions FROM staff WHERE staff_id=? AND role='Admin'"
        rows = self.execute_query(query, (admin_id,))

        if rows:
            return self._map_row_to_admin(rows[0])
        return None

    def get_all(self):
        """Fetches all administrators for dashboard management."""
        query = "SELECT staff_id, name, age, gender, permissions FROM staff WHERE role='Admin'"
        rows = self.execute_query(query)
        
        admins = []
        for row in rows:
            admins.append(self._map_row_to_admin(row))
        return admins

    def _map_row_to_admin(self, row):
        """Helper to convert database row to Admin Model instance."""
        # row indexes based on the SELECT queries above
        admin = Admin(row[0], row[1], row[2], row[3])
        if len(row) > 4 and row[4]: # permissions column
            perms = row[4].split(",")
            for p in perms:
                if p: admin.add_permission(p)
        return admin

    def add_permission(self, admin_id, permission):
        """Updates admin permissions in the database."""
        admin = self.get_admin(admin_id)
        if not admin:
            raise ValueError("Admin not found")
        
        admin.add_permission(permission)
        
        updated_perms = ",".join(admin.permissions) if hasattr(admin, 'permissions') else ""
        query = "UPDATE staff SET permissions=? WHERE staff_id=? AND role='Admin'"
        
        success = self.execute_non_query(query, (updated_perms, admin_id))
        if not success:
            raise Exception("Failed to update permissions in database")
            
        return True