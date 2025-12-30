import flet as ft
from gui.layouts.admin_layout import AdminLayout

class PatientsPage:
    def __init__(self, page: ft.Page):
        self.page = page

    def build_content(self):
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Age")),
                ft.DataColumn(ft.Text("Gender")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("P01")),
                        ft.DataCell(ft.Text("Ahmed Mohamed")),
                        ft.DataCell(ft.Text("35")),
                        ft.DataCell(ft.Text("Male")),
                        ft.DataCell(ft.Chip(ft.Text("Active"), bgcolor=ft.Colors.GREEN_100)),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("P02")),
                        ft.DataCell(ft.Text("Sarah Ali")),
                        ft.DataCell(ft.Text("28")),
                        ft.DataCell(ft.Text("Female")),
                        ft.DataCell(ft.Chip(ft.Text("Inactive"), bgcolor=ft.Colors.RED_100)),
                    ]
                ),
            ],
        )

        return ft.Column(
            spacing=20,
            controls=[
                ft.Text("Patients Management", size=22, weight="bold"),
                ft.Text("View and manage all registered patients", size=13, color=ft.Colors.GREY),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    padding=20,
                    border_radius=12,
                    content=table
                )
            ]
        )

    def build(self) -> ft.View:
        content = self.build_content()
        return ft.View(
            route="/patients",
            padding=0,
            controls=[AdminLayout(self.page, content).build()]
        )
