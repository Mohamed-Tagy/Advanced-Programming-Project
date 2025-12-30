import flet as ft

def user_layout(
    page,
    main_content,
    logout,
    overview,
    doctors,
    appointments,
):

    def menu_item(text, icon, action):
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

    sidebar = ft.Column(
        spacing=20,
        controls=[
            ft.Text("Hospital User", size=20, weight="bold"),
            ft.Divider(),

            menu_item("Overview", ft.Icons.DASHBOARD, overview),
            menu_item("Doctors", ft.Icons.MEDICAL_SERVICES, doctors),
            menu_item("Appointments", ft.Icons.EVENT, appointments),

            ft.Divider(),
            menu_item("Logout", ft.Icons.LOGOUT, logout),
        ]
    )

    # 🌟 استخدمنا Column مع scroll=True بدل Scrollable
    main_content_container = ft.Column(
        expand=True,
        spacing=0,
        scroll=True,
        controls=[main_content]
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
