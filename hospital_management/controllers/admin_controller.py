from main import Admin
from main import BaseController

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
