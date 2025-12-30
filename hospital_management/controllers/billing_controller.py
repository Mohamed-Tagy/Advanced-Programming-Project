from models.billing import Billing
from controller.base_controller import BaseController

class BillingController(BaseController):

    def create_bill(self, bill_id, patient_id, patient_name,
                    amount, description=""):
        if self.exists(bill_id):
            raise ValueError("Bill already exists")

        bill = Billing(bill_id, patient_id, patient_name, amount, description)
        self._items[bill_id] = bill
        return bill

    def make_payment(self, bill_id, amount, method="Cash", date=""):
        bill = self.get(bill_id)
        if not bill:
            raise ValueError("Bill not found")
        return bill.make_payment(amount, method, date)

    def add_charge(self, bill_id, amount, description=""):
        bill = self.get(bill_id)
        if not bill:
            raise ValueError("Bill not found")
        return bill.add_charge(amount, description)

    def apply_discount(self, bill_id, percentage, reason=""):
        bill = self.get(bill_id)
        if not bill:
            raise ValueError("Bill not found")
        return bill.apply_discount(percentage, reason)
