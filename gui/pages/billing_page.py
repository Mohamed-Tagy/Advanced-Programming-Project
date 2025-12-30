import flet as ft
from gui.layouts.admin_layout import admin_layout


def billing_page(page: ft.Page):

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Invoice ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("INV-001")),
                    ft.DataCell(ft.Text("Ahmed Mohamed")),
                    ft.DataCell(ft.Text("$250")),
                    ft.DataCell(ft.Chip(ft.Text("Paid"), bgcolor=ft.Colors.GREEN_100)),
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("INV-002")),
                    ft.DataCell(ft.Text("Sarah Ali")),
                    ft.DataCell(ft.Text("$180")),
                    ft.DataCell(ft.Chip(ft.Text("Pending"), bgcolor=ft.Colors.ORANGE_100)),
                ]
            ),
        ],
    )

    content = ft.Column(
        spacing=20,
        controls=[
            ft.Text("Billing & Payments", size=22, weight="bold"),
            ft.Text("Invoices and payment tracking", size=13, color=ft.Colors.GREY),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=12,
                content=table
            )
        ]
    )

    return ft.View(
        route="/billing",
        padding=0,
        controls=[admin_layout(page, content)]
    )
