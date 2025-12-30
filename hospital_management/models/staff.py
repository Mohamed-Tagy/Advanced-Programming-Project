from models import Person

class Staff(Person):
    def __init__(self, staff_id, name, age, gender, role,
                 phone=None, email=None, address=None):
        super().__init__(staff_id, name, age, gender, phone, email, address)
        self.__role = role

    @property
    def role(self):
        return self.__role

    def update_role(self, new_role):
        self.__role = new_role

    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "role": self.__role
        }