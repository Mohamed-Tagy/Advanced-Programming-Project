class Billing:
    def __init__(self, bill_id, patient_id, patient_name, amount, service_description=""):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.amount = amount
        self.service_description = service_description
        self.payment_status = "Pending"  # Simple: Pending or Paid
        self.paid_amount = 0  # How much has been paid so far
    
    def make_payment(self, amount_paid):
        """Record a payment"""
        if amount_paid <= 0:
            return "Payment amount must be positive"
        
        # Add to what's been paid
        self.paid_amount += amount_paid
        
        # Check if fully paid
        if self.paid_amount >= self.amount:
            self.payment_status = "Paid"
            return f"Bill {self.bill_id} is now fully paid!"
        else:
            remaining = self.amount - self.paid_amount
            return f"Payment received. ${remaining} still owed."
    
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
