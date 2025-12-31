import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.billing_controller import BillingController

def main():
    controller = BillingController()

    bill = controller.create_bill(
        bill_id="B100",
        patient_id="P100",
        patient_name="Test User",
        amount=500.0,
        description="General Checkup"
    )
    print("Created bill:", bill.to_dict())

    bill = controller.make_payment("B100", 200, method="Cash")
    print("After partial payment:", bill.to_dict())

    bill = controller.add_charge("B100", 100, "Lab Test")
    print("After adding charge:", bill.to_dict())

    bill = controller.apply_discount("B100", 10, "Promo")
    print("After applying discount:", bill.to_dict())

    bill = controller.make_payment("B100", bill.amount, method="Card")
    print("After full payment:", bill.to_dict())

if __name__ == "__main__":
    main()
