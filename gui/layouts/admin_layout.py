import flet as ft

PRIMARY = ft.Colors.BLUE_700
BG = "#F4F6F8"


def admin_layout(page: ft.Page, content: ft.Control):

    def logout(e):
        page.session.clear()
        page.go("/")

    sidebar = ft.Container(
        width=240,
        bgcolor=ft.Colors.WHITE,
        padding=15,
        border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_200)),
        content=ft.Column(
            [
                ft.Text("Hospital Admin", size=20, weight="bold", color=PRIMARY),
                ft.Divider(),

                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DASHBOARD),
                    title=ft.Text("Overview"),
                    on_click=lambda _: page.go("/admin-dashboard"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text("Patients"),
                    on_click=lambda _: page.go("/patients"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.MEDICAL_SERVICES),
                    title=ft.Text("Doctors"),
                    on_click=lambda _: page.go("/doctors"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CALENDAR_MONTH),
                    title=ft.Text("Appointments"),
                    on_click=lambda _: page.go("/appointments"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ATTACH_MONEY),
                    title=ft.Text("Billing"),
                    on_click=lambda _: page.go("/billing"),
                ),

                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED),
                    title=ft.Text("Logout"),
                    on_click=logout,
                ),
            ]
        ),
    )

    return ft.Row(
        expand=True,
        spacing=0,
        controls=[
            sidebar,
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=25,
                content=content
            )
        ]
    )
