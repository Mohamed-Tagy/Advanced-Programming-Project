import flet as ft

# ---------------- Pages ----------------
from gui.pages.login_page import LoginPage
from gui.pages.signup_page import SignupPage
from gui.pages.user_dashboard import UserDashboard
from gui.pages.admin_dashboard import AdminDashboard
from gui.pages.appointment_page import AppointmentPage  # الاسم الصح
from gui.pages.doctor_page import DoctorsPage
from gui.pages.patient_page import PatientsPage
from gui.pages.billing_page import BillingPage

def main(page: ft.Page):
    page.title = "Hospital Management System"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.theme_mode = ft.ThemeMode.LIGHT

    # ---------- Session Defaults ----------
    page.session.set("is_logged_in", False)
    page.session.set("role", None)

    # ---------- Guards ----------
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

    # ---------- Routing ----------
    def route_change(route):
        page.views.clear()

        # ---------- Public Pages ----------
        if page.route == "/":
            page.views.append(LoginPage(page).build())
        elif page.route == "/signup":
            page.views.append(SignupPage(page).build())

        # ---------- User Pages ----------
        elif page.route in ["/user-dashboard", "/user-doctors", "/user-appointments"]:
            if not require_login():
                return
            page.views.append(UserDashboard(page).build())

        # ---------- Admin Pages ----------
        elif page.route == "/admin-dashboard":
            if not require_login() or not require_admin():
                return
            page.views.append(AdminDashboard(page).build())
        elif page.route == "/appointments":
            if not require_login() or not require_admin():
                return
            page.views.append(AppointmentPage(page).build())  # الاسم الصح
        elif page.route == "/doctors":
            if not require_login() or not require_admin():
                return
            page.views.append(DoctorsPage(page).build())
        elif page.route == "/patients":
            if not require_login() or not require_admin():
                return
            page.views.append(PatientsPage(page).build())
        elif page.route == "/billing":
            if not require_login() or not require_admin():
                return
            page.views.append(BillingPage(page).build())

        page.update()

    page.on_route_change = route_change
    page.go("/")

# ---------- Run App ----------
ft.app(target=main)
