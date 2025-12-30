import flet as ft
from gui.layouts.admin_layout import admin_layout

def admin_dashboard(page: ft.Page):
    # بيانات مؤقتة بدل الـ backend
    appointments = [
        {"id": "A01", "patient": "Ahmed Mohamed", "status": "Pending"},
        {"id": "A02", "patient": "Sarah Ali", "status": "Approved"},
        {"id": "A03", "patient": "Mohamed Ali", "status": "Rejected"},
        {"id": "A04", "patient": "Hana Mohamed", "status": "Pending"},
    ]

    pending = len([a for a in appointments if a["status"] == "Pending"])
    approved = len([a for a in appointments if a["status"] == "Approved"])
    rejected = len([a for a in appointments if a["status"] == "Rejected"])

    def stat_card(title, value, color):
        return ft.Container(
            expand=True,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            content=ft.Column(
                [
                    ft.Text(title, size=14, color=ft.Colors.GREY_600),
                    ft.Text(value, size=26, weight="bold", color=color),
                ]
            ),
        )

    recent_requests = ft.Column(
        controls=[
            ft.Text("Recent Requests", size=18, weight="bold"),
            *[
                ft.Row(
                    [
                        ft.Text(a["patient"], expand=True),
                        ft.Text(a["status"], color={
                            "Pending": ft.Colors.ORANGE,
                            "Approved": ft.Colors.GREEN,
                            "Rejected": ft.Colors.RED
                        }[a["status"]]),
                    ]
                )
                for a in appointments[:3]
            ],
        ]
    )

    content = ft.Column(
        spacing=25,
        controls=[
            ft.Text("Admin Overview", size=24, weight="bold"),

            ft.Row(
                spacing=20,
                controls=[
                    stat_card("Pending Requests", pending, ft.Colors.ORANGE),
                    stat_card("Approved", approved, ft.Colors.GREEN),
                    stat_card("Rejected", rejected, ft.Colors.RED),
                ],
            ),

            ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=12,
                content=recent_requests,
            ),
        ],
    )

    return ft.View(
        route="/admin-dashboard",
        padding=0,
        controls=[admin_layout(page, content)],
    )
