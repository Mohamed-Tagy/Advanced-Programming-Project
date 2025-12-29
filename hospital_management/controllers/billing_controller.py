from models.billing import Billing

class BillingController:
    def __init__(self):
        self.bills = []

    def add_bill(self, bill: Billing):
        self.bills.append(bill)

    def get_all_bills(self):
        return self.bills
