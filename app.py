import flet as ft
from gui.pages.login_page import login_page
from gui.pages.signup_page import signup_page
from gui.pages.user_dashboard import user_dashboard
from gui.pages.admin_dashboard import admin_dashboard
from gui.pages.appointment_page import appointments_page
from gui.pages.doctor_page import doctors_page
from gui.pages.patient_page import patients_page
from gui.pages.billing_page import billing_page


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
            page.views.append(login_page(page))
        elif page.route == "/signup":
            page.views.append(signup_page(page))

        # ---------- User Pages ----------
        elif page.route in ["/user-dashboard", "/user-doctors", "/user-appointments"]:
            if not require_login():
                return
            page.views.append(user_dashboard(page))

        # ---------- Admin Pages ----------
        elif page.route == "/admin-dashboard":
            if not require_login() or not require_admin():
                return
            page.views.append(admin_dashboard(page))
        elif page.route == "/appointments":
            if not require_login():
                return
            page.views.append(appointments_page(page))
        elif page.route == "/doctors":
            if not require_login() or not require_admin():
                return
            page.views.append(doctors_page(page))
        elif page.route == "/patients":
            if not require_login() or not require_admin():
                return
            page.views.append(patients_page(page))
        elif page.route == "/billing":
            if not require_login() or not require_admin():
                return
            page.views.append(billing_page(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(target=main)
