import flet as ft

PRIMARY = ft.Colors.BLUE_700
BG = "#F4F6F8"

class AdminLayout:
    def __init__(self, page: ft.Page, content: ft.Control):
        self.page = page
        self.content = content

    def logout(self, e):
        self.page.session.clear()
        self.page.go("/")

    def build_sidebar(self):
        return ft.Container(
            width=240,
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_200)),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO, 
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=10, bottom=10),
                        content=ft.Text("Hospital Admin", size=20, weight="bold", color=PRIMARY),
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_100),

                    self.nav_item(ft.Icons.DASHBOARD, "Overview", "/admin-dashboard"),
                    self.nav_item(ft.Icons.PERSON, "Patients", "/patients"),
                    self.nav_item(ft.Icons.MEDICAL_SERVICES, "Doctors", "/doctors"),
                    self.nav_item(ft.Icons.CALENDAR_MONTH, "Appointments", "/appointments"),
                    self.nav_item(ft.Icons.ATTACH_MONEY, "Billing", "/billing"),

                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Divider(height=1, color=ft.Colors.GREY_100),
                    
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400),
                        title=ft.Text("Logout", color=ft.Colors.RED_400),
                        on_click=self.logout,
                    ),
                ]
            ),
        )

    def nav_item(self, icon, title, route):
        """Helper to create consistent nav links with active state logic potential"""
        return ft.ListTile(
            leading=ft.Icon(icon),
            title=ft.Text(title),
            on_click=lambda _: self.page.go(route),
            hover_color=ft.Colors.BLUE_50,
        )

    def build(self):
        return ft.Row(
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START, 
            controls=[
                self.build_sidebar(),
                ft.Container(
                    expand=True,
                    bgcolor=BG,
                    padding=25,
                    alignment=ft.alignment.top_left, 
                    content=ft.Column(
                        [self.content],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    )
                )
            ]
        )