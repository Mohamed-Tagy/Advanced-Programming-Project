# hospital_management/tests/test_manual_admin.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from hospital_management.controllers.admin_controller import AdminController

def main():
    # Initialize controller
    controller = AdminController()

    # Create admin
    try:
        admin = controller.create_admin("A100", "SuperAdmin", 30, "M")
        print("Created admin:", admin.to_dict())
    except Exception as e:
        print("Error creating admin:", e)
        admin = controller.get_admin("A100")
        print("Fetched existing admin:", admin.to_dict())

    # Add permissions
    try:
        controller.add_permission("A100", "Manage Users")
        controller.add_permission("A100", "View Reports")
        print("Permissions added.")
    except Exception as e:
        print("Error adding permissions:", e)

    # Fetch admin again and display
    admin = controller.get_admin("A100")
    print("After adding permissions:", admin.to_dict())

    # Try adding duplicate permission
    controller.add_permission("A100", "Manage Users")
    admin = controller.get_admin("A100")
    print("After trying duplicate permission:", admin.to_dict())

if __name__ == "__main__":
    main()
