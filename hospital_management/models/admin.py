from models.staff import Staff

class Admin(Staff):
    def __init__(self, staff_id, name, age, gender,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, "Admin", phone, email, address)
        self.__permissions = []   # private (security-critical)

    def add_permission(self, permission):
        if permission not in self.__permissions:
            self.__permissions.append(permission)

    def remove_permission(self, permission):
        if permission in self.__permissions:
            self.__permissions.remove(permission)

    def has_permission(self, permission):
        return permission in self.__permissions

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "permissions": list(self.__permissions)  # safe copy
        })
        return data