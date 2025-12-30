import flet as ft

class UserLayout:
    def __init__(self, page, main_content, logout, overview, doctors, appointments):
        self.page = page
        self.main_content = main_content
        self.logout = logout
        self.overview = overview
        self.doctors = doctors
        self.appointments = appointments

    def menu_item(self, text, icon, action):
        return ft.TextButton(
            on_click=action,
            style=ft.ButtonStyle(
                alignment=ft.alignment.center_left,
                padding=20
            ),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(icon, size=20),
                    ft.Text(text),
                ]
            ),
        )

    def build(self):
        sidebar = ft.Column(
            spacing=20,
            controls=[
                ft.Text("Hospital User", size=20, weight="bold"),
                ft.Divider(),

                self.menu_item("Overview", ft.Icons.DASHBOARD, self.overview),
                self.menu_item("Doctors", ft.Icons.MEDICAL_SERVICES, self.doctors),
                self.menu_item("Appointments", ft.Icons.EVENT, self.appointments),

                ft.Divider(),
                self.menu_item("Logout", ft.Icons.LOGOUT, self.logout),
            ]
        )

        main_content_container = ft.Column(
            expand=True,
            spacing=0,
            scroll=True,
            controls=[self.main_content]
        )

        return ft.Row(
            expand=True,
            controls=[
                ft.Container(
                    width=240,
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    content=sidebar
                ),
                ft.Container(
                    expand=True,
                    padding=30,
                    alignment=ft.alignment.top_left,
                    content=main_content_container
                ),
            ]
        )
