import flet as ft
from gui.layouts.admin_layout import AdminLayout
from backend.controllers.billing_controller import BillingController
import time

class BillingPage:
    def __init__(self, page: ft.Page, billing_controller: BillingController):
        self.page = page
        self.billing_controller = billing_controller
        self.table_container = ft.Column(scroll=ft.ScrollMode.AUTO)
        self.rev_realized_text = ft.Text("$0.00", size=28, weight="bold", color=ft.Colors.GREEN_900)
        self.pending_rev_text = ft.Text("$0.00", size=28, weight="bold", color=ft.Colors.ORANGE_900)

    def show_payment_dialog(self, bill_id):
        """Opens a dialog to process a payment."""
        amt_input = ft.TextField(label="Payment Amount", prefix_text="$", keyboard_type=ft.KeyboardType.NUMBER)
        
        def confirm_payment(e):
            try:
                if not amt_input.value: return
                self.billing_controller.make_payment(bill_id, float(amt_input.value))
                self.page.dialog.open = False
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Payment for {bill_id} successful!"), bgcolor="green")
                self.page.snack_bar.open = True
                self.update_ui() 
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor="red")
                self.page.snack_bar.open = True
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Process Payment: {bill_id}"),
            content=amt_input,
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.close_dialog()),
                ft.ElevatedButton("Confirm Payment", on_click=confirm_payment, bgcolor=ft.Colors.BLUE_700, color="white")
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def show_create_bill_dialog(self, e):
        """Dialog to generate a new invoice."""
        p_id_input = ft.TextField(label="Patient ID (e.g. PAT-123)")
        amount_input = ft.TextField(label="Amount", prefix_text="$", keyboard_type=ft.KeyboardType.NUMBER)

        def save_bill(e):
            try:
                if p_id_input.value and amount_input.value:
                    new_id = f"INV-{int(time.time())}"
                    self.billing_controller.create_bill(new_id, p_id_input.value, float(amount_input.value))
                    self.page.dialog.open = False
                    self.update_ui()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Generate New Invoice"),
            content=ft.Column([p_id_input, amount_input], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.close_dialog()),
                ft.ElevatedButton("Create Bill", on_click=save_bill, bgcolor=ft.Colors.BLUE_700, color="white")
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def update_ui(self):
        """Refreshes statistics and the data table."""
        all_bills = self.billing_controller.get_all()
        
        total_rev = sum(b.amount for b in all_bills if b.payment_status == "Paid")
        pending_rev = sum(b.amount for b in all_bills if b.payment_status != "Paid")
        
        self.rev_realized_text.value = f"${total_rev:,.2f}"
        self.pending_rev_text.value = f"${pending_rev:,.2f}"
        
        self.table_container.controls = [self.create_data_table(all_bills)]
        self.page.update()

    def create_data_table(self, bills):
        rows = []
        for bill in bills:
            is_paid = bill.payment_status == "Paid"
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(bill.bill_id), weight="bold")),
                        ft.DataCell(ft.Text(str(bill.patient_id))),
                        ft.DataCell(ft.Text(f"${bill.amount:,.2f}")),
                        ft.DataCell(
                            ft.Chip(
                                label=ft.Text(bill.payment_status, size=11, color=ft.Colors.WHITE if is_paid else ft.Colors.BLACK),
                                bgcolor=ft.Colors.GREEN_600 if is_paid else ft.Colors.ORANGE_300,
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.PAYMENT,
                                    tooltip="Process Payment",
                                    icon_color=ft.Colors.BLUE_700,
                                    visible=not is_paid,
                                    on_click=lambda _, bid=bill.bill_id: self.show_payment_dialog(bid)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.PRINT,
                                    tooltip="Print Invoice",
                                    on_click=lambda _, bid=bill.bill_id: print(f"Printing {bid}...")
                                )
                            ])
                        ),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Invoice ID")),
                ft.DataColumn(ft.Text("Patient ID")),
                ft.DataColumn(ft.Text("Total Amount")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=rows,
            heading_row_color=ft.Colors.GREY_100,
            column_spacing=50,
        )

    def build_content(self):
        all_bills = self.billing_controller.get_all()
        total_rev = sum(b.amount for b in all_bills if b.payment_status == "Paid")
        pending_rev = sum(b.amount for b in all_bills if b.payment_status != "Paid")


        self.rev_realized_text.value = f"${total_rev:,.2f}"
        self.pending_rev_text.value = f"${pending_rev:,.2f}"
        self.table_container.controls = [self.create_data_table(all_bills)]
        
        return ft.Column(
            expand=True,
            spacing=25,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Text("Financial Management", size=28, weight="bold"),
                            ft.Text("Track hospital revenue and manage patient accounts", color=ft.Colors.GREY_600),
                        ]),
                        ft.ElevatedButton(
                            "New Invoice", 
                            icon=ft.Icons.ADD_CARD, 
                            bgcolor=ft.Colors.BLUE_700, 
                            color="white",
                            on_click=self.show_create_bill_dialog
                        )
                    ]
                ),
                ft.ResponsiveRow(
                    spacing=20,
                    controls=[
                        ft.Container(
                            col={"md": 6},
                            bgcolor=ft.Colors.GREEN_50,
                            padding=20,
                            border_radius=12,
                            content=ft.Column([
                                ft.Text("Revenue Realized", color=ft.Colors.GREEN_800, weight="w500"),
                                self.rev_realized_text
                            ], spacing=5)
                        ),
                        ft.Container(
                            col={"md": 6},
                            bgcolor=ft.Colors.ORANGE_50,
                            padding=20,
                            border_radius=12,
                            content=ft.Column([
                                ft.Text("Pending Invoices", color=ft.Colors.ORANGE_800, weight="w500"),
                                self.pending_rev_text
                            ], spacing=5)
                        ),
                    ]
                ),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    padding=15,
                    border_radius=12,
                    expand=True,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    content=ft.Column([self.table_container], scroll=ft.ScrollMode.ALWAYS)
                )
            ]
        )

    def build(self) -> ft.View:
        return ft.View(
            route="/billing",
            padding=0,
            bgcolor="#F4F6F8",
            controls=[AdminLayout(self.page, self.build_content()).build()]
        )