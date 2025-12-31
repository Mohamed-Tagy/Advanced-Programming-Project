import flet as ft

# ---------------- Pages ----------------
from gui.pages.login_page import LoginPage
from gui.pages.signup_page import SignupPage
from gui.pages.user_dashboard import UserDashboard
from gui.pages.admin_dashboard import AdminDashboard
from gui.pages.appointment_page import AppointmentPage
from gui.pages.doctor_page import DoctorsPage
from gui.pages.patient_page import PatientsPage
from gui.pages.billing_page import BillingPage

# ---------------- Backend Controllers ----------------
from backend.controllers.patient_controller import PatientController
from backend.controllers.doctor_controller import DoctorController
from backend.controllers.appointment_controller import AppointmentController
from backend.controllers.admin_controller import AdminController
from backend.controllers.billing_controller import BillingController
from backend.controllers.auth_controller import AuthController 

def main(page: ft.Page):
    page.title = "Hospital Management System"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.window_width = 1200
    page.window_height = 800

    # ---------- Initialize Controllers ----------
    patient_ctrl = PatientController()
    doctor_ctrl = DoctorController()
    admin_ctrl = AdminController()
    billing_ctrl = BillingController()
    appointment_ctrl = AppointmentController()
    auth_ctrl = AuthController(patient_ctrl, admin_ctrl)

    # ---------- Guards (Security) ----------
    def require_login():
        if not page.session.get("is_logged_in"):
            page.go("/")
            return False
        return True

    def require_admin():
        if page.session.get("role") != "admin":
            page.go("/user-dashboard")
            return False
        return True

    # ---------- Routing Logic ----------
    def route_change(e):
        page.views.clear()
        route = page.route

        # 1. Public Access Pages
        if route == "/":
            page.views.append(LoginPage(page, auth_ctrl).build())
            
        elif route == "/signup":
            page.views.append(SignupPage(page, auth_ctrl).build())

        # 2. Patient / User Area (Guarded)
        elif route.startswith("/user-"):
            if not require_login():
                return
            
            # Create the Dashboard instance
            dashboard = UserDashboard(
                page, 
                doctor_ctrl, 
                appointment_ctrl, 
                patient_ctrl
            )

            # Determine which internal view to show based on the route
            if route == "/user-dashboard":
                dashboard.show_overview()
            elif route == "/user-doctors":
                dashboard.show_doctors()
            elif route == "/user-appointments":
                dashboard.show_appointments()
            elif route == "/user-settings":
                dashboard.show_settings()
            
            page.views.append(dashboard.build())

        # 3. Administrative Area (Guarded)
        elif route in ["/admin-dashboard", "/appointments", "/doctors", "/patients", "/billing"]:
            if not require_login() or not require_admin():
                return

            if route == "/admin-dashboard":
                page.views.append(AdminDashboard(page, appointment_ctrl, admin_ctrl).build())
            elif route == "/appointments":
                page.views.append(AppointmentPage(page, appointment_ctrl).build())
            elif route == "/doctors":
                page.views.append(DoctorsPage(page, doctor_ctrl).build())
            elif route == "/patients":
                page.views.append(PatientsPage(page, patient_ctrl).build())
            elif route == "/billing":
                page.views.append(BillingPage(page, billing_ctrl).build())

        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)