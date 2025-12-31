from hospital_management.models.person import Person

class Admin(Person):
    def __init__(self, admin_id, name, age, gender,
                 phone=None, email=None, address=None):
        super().__init__(admin_id, name, age, gender, phone, email, address)
        self.__permissions = []

    def add_permission(self, permission):
        if permission not in self.__permissions:
            self.__permissions.append(permission)

    def remove_permission(self, permission):
        if permission in self.__permissions:
            self.__permissions.remove(permission)

    def has_permission(self, permission):
        return permission in self.__permissions

    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "permissions": list(self.__permissions)
        }
