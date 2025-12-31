from hospital_management.models.admin import Admin
from hospital_management.controllers.base_controller import BaseController
from hospital_management.database.db_manager import Database

class AdminController(BaseController):
    def __init__(self):
        super().__init__()
        self.db = Database()

    def create_admin(self, admin_id, name, age, gender,
                     phone=None, email=None, address=None):
        if self.exists(admin_id):
            raise ValueError("Admin already exists")

        admin = Admin(admin_id, name, age, gender, phone, email, address)
        self._items[admin_id] = admin

        self.db.execute(
            "INSERT INTO staff (staff_id, name, age, gender, role, permissions) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (admin_id, name, age, gender, "Admin", "")
        )
        return admin

    def get_admin(self, admin_id):
        if admin_id in self._items:
            return self._items[admin_id]

        row = self.db.fetchone(
            "SELECT staff_id, name, age, gender, permissions FROM staff WHERE staff_id=?",
            (admin_id,)
        )
        if row:
            admin = Admin(row[0], row[1], row[2], row[3])
            perms = row[4].split(",") if row[4] else []
            for p in perms:
                admin.add_permission(p)
            self._items[admin_id] = admin
            return admin
        return None

    def add_permission(self, admin_id, permission):
        admin = self.get_admin(admin_id)
        if not admin:
            raise ValueError("Admin not found")
        admin.add_permission(permission)
        self.db.execute(
            "UPDATE staff SET permissions=? WHERE staff_id=?",
            (",".join(admin.to_dict()["permissions"]), admin_id)
        )
