import flet as ft
from gui.layouts.admin_layout import AdminLayout

class DoctorsPage:
    def __init__(self, page: ft.Page):
        self.page = page

    def build_content(self):
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Doctor Name")),
                ft.DataColumn(ft.Text("Specialty")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("D01")),
                        ft.DataCell(ft.Text("Dr. Khaled Hassan")),
                        ft.DataCell(ft.Text("Cardiology")),
                        ft.DataCell(ft.Chip(ft.Text("Active"), bgcolor=ft.Colors.GREEN_100)),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("D02")),
                        ft.DataCell(ft.Text("Dr. Mona Adel")),
                        ft.DataCell(ft.Text("Dermatology")),
                        ft.DataCell(ft.Chip(ft.Text("On Leave"), bgcolor=ft.Colors.ORANGE_100)),
                    ]
                ),
            ],
        )

        return ft.Column(
            spacing=20,
            controls=[
                ft.Text("Doctors Management", size=22, weight="bold"),
                ft.Text("Manage doctors and specialties", size=13, color=ft.Colors.GREY),
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
            route="/doctors",
            padding=0,
            controls=[AdminLayout(self.page, content).build()]
        )
