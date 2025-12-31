from hospital_management.models.billing import Billing
from hospital_management.controllers.base_controller import BaseController
from hospital_management.database.db_manager import Database

class BillingController(BaseController):
    def __init__(self):
        super().__init__()
        self.db = Database()

    def create_bill(self, bill_id, patient_id, patient_name, amount, description=""):
        if self.exists(bill_id):
            raise ValueError("Bill already exists")

        bill = Billing(bill_id, patient_id, patient_name, amount, description)
        self._items[bill_id] = bill

        self.db.execute(
            "INSERT INTO bills (bill_id, patient_id, patient_name, amount, service_description, payment_status) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (bill_id, patient_id, patient_name, amount, description, bill.payment_status)
        )
        return bill

    def get_bill(self, bill_id):
        if bill_id in self._items:
            return self._items[bill_id]

        row = self.db.fetchone(
            "SELECT bill_id, patient_id, patient_name, amount, service_description, payment_status, payment_date, payment_method "
            "FROM bills WHERE bill_id=?",
            (bill_id,)
        )
        if row:
            bill = Billing(row[0], row[1], row[2], row[3], row[4])
            bill.payment_status = row[5]
            bill.payment_date = row[6]
            bill.payment_method = row[7]
            self._items[bill_id] = bill
            return bill
        return None

    def make_payment(self, bill_id, amount, method="Cash", date=None):
        bill = self.get_bill(bill_id)
        if not bill:
            raise ValueError("Bill not found")

        bill.make_payment(amount, method, date)
        self.db.execute(
            "UPDATE bills SET amount=?, payment_status=?, payment_date=?, payment_method=? WHERE bill_id=?",
            (bill.amount, bill.payment_status, bill.payment_date, bill.payment_method, bill.bill_id)
        )
        return bill

    def add_charge(self, bill_id, amount, description=""):
        bill = self.get_bill(bill_id)
        if not bill:
            raise ValueError("Bill not found")

        bill.add_charge(amount, description)
        self.db.execute(
            "UPDATE bills SET amount=?, service_description=?, payment_status=? WHERE bill_id=?",
            (bill.amount, bill.service_description, bill.payment_status, bill.bill_id)
        )
        return bill

    def apply_discount(self, bill_id, percentage, reason=""):
        bill = self.get_bill(bill_id)
        if not bill:
            raise ValueError("Bill not found")

        bill.apply_discount(percentage, reason)
        self.db.execute(
            "UPDATE bills SET amount=? WHERE bill_id=?",
            (bill.amount, bill.bill_id)
        )
        return bill
