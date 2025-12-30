import flet as ft
from gui.layouts.admin_layout import admin_layout

def appointments_page(page: ft.Page):
    # بيانات مؤقتة
    appointments = [
        {"id": "A01", "patient": "Ahmed Mohamed", "doctor": "Dr. Khaled", "date": "2025-01-10", "status": "Pending"},
        {"id": "A02", "patient": "Sarah Ali", "doctor": "Dr. Mona", "date": "2025-01-12", "status": "Approved"},
        {"id": "A03", "patient": "Mohamed Ali", "doctor": "Dr. Khaled", "date": "2025-01-15", "status": "Rejected"},
    ]

    def update_status(index, new_status):
        appointments[index]["status"] = new_status
        page.update()

    def status_chip(status):
        color = {
            "Pending": ft.Colors.ORANGE_100,
            "Approved": ft.Colors.GREEN_100,
            "Rejected": ft.Colors.RED_100,
        }
        return ft.Chip(ft.Text(status), bgcolor=color[status])

    rows = []
    for i, ap in enumerate(appointments):
        action_buttons = []
        if ap["status"] == "Pending":
            action_buttons = [
                ft.IconButton(
                    ft.Icons.CHECK,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Approve",
                    on_click=lambda e, i=i: update_status(i, "Approved"),
                ),
                ft.IconButton(
                    ft.Icons.CLOSE,
                    icon_color=ft.Colors.RED,
                    tooltip="Reject",
                    on_click=lambda e, i=i: update_status(i, "Rejected"),
                ),
            ]

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(ap["id"])),
                    ft.DataCell(ft.Text(ap["patient"])),
                    ft.DataCell(ft.Text(ap["doctor"])),
                    ft.DataCell(ft.Text(ap["date"])),
                    ft.DataCell(status_chip(ap["status"])),
                    ft.DataCell(ft.Row(action_buttons, spacing=5)),
                ]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Action")),
        ],
        rows=rows,
        heading_row_color=ft.Colors.GREY_200,
        border=ft.border.all(1, ft.Colors.GREY_300),
        data_row_min_height=55,
        heading_row_height=50,
        column_spacing=20,
        divider_thickness=1,
    )

    # Column بدون expand، الجدول يبدأ من الأعلى
    content = ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        alignment="start",
        controls=[
            ft.Text("Appointment Requests", size=24, weight="bold"),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=12,
                content=table,
            ),
        ],
    )

    return ft.View(
        route="/appointments",
        padding=0,
        controls=[admin_layout(page, content)],
    )
