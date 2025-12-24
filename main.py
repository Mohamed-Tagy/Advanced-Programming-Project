from abc import ABC, abstractmethod
class Person(ABC):
  def __init__(self, name, id, phone):
    self.name = name
    self.id = id
    self.phone = phone
  def change_phone(self,new_phone):
    self.phone = new_phone
  @abstarctmethod
  def to_dict(self):
    pass
  
