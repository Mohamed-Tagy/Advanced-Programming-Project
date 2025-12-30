class Billing:
    """Billing class for hospital payments"""
    
    def __init__(self, bill_id, patient_id, patient_name, amount, service_description=""):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.amount = amount
        self.service_description = service_description
        self.payment_status = "Pending"  # Pending, Paid, Partially Paid, Overdue
        self.payment_date = None
        self.payment_method = ""
    
    def make_payment(self, amount_paid, payment_method="Cash", payment_date=""):
        """Record a payment"""
        if amount_paid <= 0:
            return "Payment amount must be positive"
        
        if amount_paid > self.amount:
            return f"Payment (${amount_paid}) exceeds bill amount (${self.amount})"
        
        self.amount -= amount_paid
        self.payment_method = payment_method
        
        if payment_date:
            self.payment_date = payment_date
        else:
            from datetime import datetime
            self.payment_date = datetime.now().strftime("%Y-%m-%d")
        
        if self.amount == 0:
            self.payment_status = "Fully Paid"
        else:
            self.payment_status = "Partially Paid"
        
        return (f"Payment of ${amount_paid} received from {self.patient_name}\n"
                f"Remaining balance: ${self.amount}\n"
                f"Status: {self.payment_status}")
    
    def add_charge(self, additional_amount, description=""):
        """Add additional charge to bill"""
        self.amount += additional_amount
        
        if description:
            self.service_description += f"; {description}"
        
        if self.payment_status == "Fully Paid":
            self.payment_status = "Pending"
        
        return f"Added ${additional_amount} charge. New total: ${self.amount}"
    
    def apply_discount(self, discount_percentage, reason=""):
        """Apply discount to bill"""
        if discount_percentage <= 0 or discount_percentage > 100:
            return "Discount percentage must be between 1-100"
        
        discount_amount = (self.amount * discount_percentage) / 100
        self.amount -= discount_amount
        
        discount_note = f" ({reason})" if reason else ""
        return f"Applied {discount_percentage}% discount{discount_note}. New total: ${self.amount:.2f}"
    
    def get_bill_summary(self):
        """Get billing summary"""
        return (f"Bill ID: {self.bill_id}\n"
                f"Patient: {self.patient_name} (ID: {self.patient_id})\n"
                f"Service: {self.service_description}\n"
                f"Amount Due: ${self.amount:.2f}\n"
                f"Status: {self.payment_status}\n"
                f"Payment Date: {self.payment_date if self.payment_date else 'Not paid yet'}\n"
                f"Payment Method: {self.payment_method if self.payment_method else 'Not specified'}")
    
    def is_paid(self):
        """Check if bill is fully paid"""
        if self.payment_status == "Fully Paid":
            return f"Bill {self.bill_id} is fully paid"
        else:
            return f"Bill {self.bill_id} has ${self.amount:.2f} remaining"
    
    def __str__(self):
        return f"Bill {self.bill_id}: {self.patient_name} - ${self.amount} ({self.payment_status})"
