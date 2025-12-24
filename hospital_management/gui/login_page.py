import flet as ft
from controllers.auth_controller import AuthController


class LoginPage:
    def __init__(self, page: ft.Page, app_controller):
        self.page = page
        self.app_controller = app_controller
        self.auth_controller = AuthController(app_controller.db)

        # Form fields
        self.email_input = ft.TextField(label="Email", width=300)
        self.password_input = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
        self.error_text = ft.Text("", color=ft.colors.RED)

    def build(self):
        return ft.Column(
            [
                ft.Text("Hospital Management System", size=30, weight=ft.FontWeight.BOLD),
                ft.Column(
                    [
                        self.email_input,
                        self.password_input,
                        self.error_text,
                        ft.ElevatedButton("Login", on_click=self.on_login),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def on_login(self, e):
        email = self.email_input.value
        password = self.password_input.value

        if not email or not password:
            self.error_text.value = "Please enter both email and password."
            self.page.update()
            return

        # Call auth controller
        user = self.auth_controller.login(email, password)
        if user:
            self.error_text.value = ""
            self.page.update()
            # Navigate to dashboard based on role
            self.app_controller.clear_page()
            if user["role"] == "admin":
                from gui.admin_dashboard import AdminDashboard
                self.page.add(AdminDashboard(self.page, self.app_controller).build())
            else:
                from gui.user_dashboard import UserDashboard
                self.page.add(UserDashboard(self.page, self.app_controller).build())
        else:
            self.error_text.value = "Invalid email or password."
            self.page.update()
