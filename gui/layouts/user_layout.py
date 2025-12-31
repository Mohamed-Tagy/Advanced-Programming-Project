import flet as ft

class UserLayout:
    def __init__(self, page, main_content, current_route, logout, overview, doctors, appointments, settings):
        self.page = page
        self.main_content = main_content
        self.current_route = current_route  
        self.logout = logout
        self.overview = overview
        self.doctors = doctors
        self.appointments = appointments
        self.settings = settings

    def menu_item(self, text, icon, action, route_name):
        is_active = self.current_route == route_name
        
        return ft.Container(
            content=ft.TextButton(
                on_click=action,
                url="", 
                style=ft.ButtonStyle(
                    color={
                        ft.ControlState.DEFAULT: ft.Colors.BLUE_700 if is_active else ft.Colors.BLACK54,
                        ft.ControlState.HOVERED: ft.Colors.BLUE_800,
                    },
                    bgcolor={
                        ft.ControlState.DEFAULT: ft.Colors.BLUE_50 if is_active else ft.Colors.TRANSPARENT,
                        ft.ControlState.HOVERED: ft.Colors.BLUE_100,
                    },
                    shape=ft.RoundedRectangleBorder(radius=10),
                    alignment=ft.alignment.center_left,
                ),
                content=ft.Container(
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    content=ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(icon, size=22),
                            ft.Text(text, size=15, weight=ft.FontWeight.W_500),
                        ]
                    )
                ),
            ),
        )

    def build(self):
        sidebar_items = ft.Column(
            spacing=5,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Container(
                    padding=ft.padding.only(bottom=20, left=10),
                    content=ft.Column([
                        ft.Text("Patient Portal", size=22, weight="bold", color=ft.Colors.BLUE_900),
                        ft.Text("Hospital Management", size=12, color=ft.Colors.GREY_600),
                    ], spacing=0)
                ),
                self.menu_item("Overview", ft.Icons.DASHBOARD_ROUNDED, self.overview, "/user-dashboard"),
                self.menu_item("Find Doctors", ft.Icons.LOCAL_HOSPITAL_ROUNDED, self.doctors, "/user-doctors"),
                self.menu_item("My Appointments", ft.Icons.CALENDAR_MONTH_ROUNDED, self.appointments, "/user-appointments"),
                self.menu_item("Settings", ft.Icons.SETTINGS_OUTLINED, self.settings, "/user-settings"),
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    padding=ft.padding.only(top=10),
                    border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200)),
                    content=self.menu_item("Logout", ft.Icons.LOGOUT_ROUNDED, self.logout, "/logout")
                ),
            ]
        )

        return ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
            controls=[
                ft.Container(
                    width=260,
                    padding=25,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_100)),
                    content=sidebar_items
                ),
                ft.Container(
                    expand=True,
                    padding=40,
                    bgcolor="#F8FAFC",
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[self.main_content] 
                    )
                ),
            ]
        )