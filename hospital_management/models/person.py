from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, person_id, name, age, gender, phone=None, email=None, address=None):
        self.__person_id = person_id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address

    @property
    def person_id(self):
        return self.__person_id

    def update_contact(self, phone=None, email=None, address=None):
        if phone is not None:
            self.phone = phone
        if email is not None:
            self.email = email
        if address is not None:
            self.address = address

    @abstractmethod
    def to_dict(self) -> dict:
        """Return a dictionary representation of the person"""
        return {
            "id": self.person_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    def __str__(self):
        return f"{self.name} (ID: {self.__person_id})"
