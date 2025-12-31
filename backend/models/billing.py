class Billing:
    """Billing class for hospital payments"""

    def __init__(self, bill_id, patient_id, patient_name, amount, service_description=""):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.amount = amount
        self.service_description = service_description
        self.payment_status = "Pending"  
        self.payment_date = None
        self.payment_method = None

    def make_payment(self, amount_paid, method="Cash", payment_date=None):
        if amount_paid <= 0:
            raise ValueError("Payment amount must be positive")
        if amount_paid > self.amount:
            raise ValueError("Payment exceeds bill amount")

        self.amount -= amount_paid
        self.payment_method = method
        from datetime import datetime
        self.payment_date = payment_date if payment_date else datetime.now().strftime("%Y-%m-%d")

        if self.amount == 0:
            self.payment_status = "Fully Paid"
        else:
            self.payment_status = "Partially Paid"
        return self

    def add_charge(self, amount, description=""):
        self.amount += amount
        if description:
            if self.service_description:
                self.service_description += f"; {description}"
            else:
                self.service_description = description
        if self.payment_status == "Fully Paid":
            self.payment_status = "Pending"
        return self

    def apply_discount(self, percentage, reason=""):
        if percentage <= 0 or percentage > 100:
            raise ValueError("Discount must be between 1-100")
        discount_amount = (self.amount * percentage) / 100
        self.amount -= discount_amount
        return self

    def to_dict(self):
        return {
            "bill_id": self.bill_id,
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "amount": self.amount,
            "service_description": self.service_description,
            "payment_status": self.payment_status,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method
        }
