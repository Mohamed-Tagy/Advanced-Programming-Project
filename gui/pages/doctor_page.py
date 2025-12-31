import flet as ft
from gui.layouts.admin_layout import AdminLayout
from backend.controllers.doctor_controller import DoctorController
import time

class DoctorsPage:
    def __init__(self, page: ft.Page, doctor_controller: DoctorController):
        self.page = page
        self.doctor_controller = doctor_controller
        self.search_field = ft.TextField(
            label="Search by name or specialty",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.update_table,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
        self.table_container = ft.Column(scroll=ft.ScrollMode.AUTO)

    def update_table(self, e=None):
        """Refreshes the doctor list with filtering."""
        self.table_container.controls = [self.create_data_table()]
        self.page.update()

    
    def toggle_status(self, doctor_id, current_status):
        """Toggles the admission status: Admitted (Green) <-> Discharged (Red)."""
        try:
            new_status = "Discharged" if current_status == "Admitted" else "Admitted"
            
            if hasattr(self.doctor_controller, 'update_status'):
                self.doctor_controller.update_status(doctor_id, new_status)
            
            self.update_table()
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Doctor is now {new_status}"),
                bgcolor=ft.Colors.GREEN_700 if new_status == "Admitted" else ft.Colors.RED_700
            )
            self.page.snack_bar.open = True
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor="red")
            self.page.snack_bar.open = True
        self.page.update()

    def show_add_doctor_dialog(self, e):
        """Opens the dialog to register a new doctor."""
        name_ref = ft.Ref[ft.TextField]()
        spec_ref = ft.Ref[ft.TextField]()
        fee_ref = ft.Ref[ft.TextField]()

        def save_new_doc(_):
            if not name_ref.current.value or not spec_ref.current.value:
                return
            try:
                new_id = f"DOC-{int(time.time())}"
                self.doctor_controller.create_doctor(
                    doctor_id=new_id,
                    name=name_ref.current.value,
                    specialty=spec_ref.current.value,
                    fee=float(fee_ref.current.value or 0)
                )
                self.page.dialog.open = False
                self.update_table()
                self.notify(f"Dr. {name_ref.current.value} registered.", ft.Colors.GREEN)
            except Exception as ex:
                self.notify(f"Error: {str(ex)}", ft.Colors.RED)
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Register New Doctor"),
            content=ft.Column([
                ft.TextField(ref=name_ref, label="Full Name"),
                ft.TextField(ref=spec_ref, label="Specialty"),
                ft.TextField(ref=fee_ref, label="Fee", prefix_text="$", value="50.0"),
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Register", on_click=save_new_doc, bgcolor=ft.Colors.BLUE_700, color="white")
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    # ----------------  ----------------
    def show_fee_dialog(self, doctor_id):
        fee_input = ft.TextField(label="New Fee", prefix_text="$", keyboard_type=ft.KeyboardType.NUMBER)
        
        def save_fee(_):
            try:
                if fee_input.value:
                    self.doctor_controller.set_fee(doctor_id, float(fee_input.value))
                    self.page.dialog.open = False
                    self.update_table()
                    self.notify("Fee updated.", ft.Colors.GREEN)
            except Exception as ex:
                self.notify(f"Error: {str(ex)}", ft.Colors.RED)
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Update Fee"),
            content=fee_input,
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Update", on_click=save_fee, bgcolor=ft.Colors.BLUE_700, color="white")
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self, e=None):
        self.page.dialog.open = False
        self.page.update()

    def notify(self, msg, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        self.page.snack_bar.open = True

    # ---------------- UI Construction ----------------
    def create_data_table(self):
        rows = []
        query = self.search_field.value.lower() if self.search_field.value else ""
        doctors = self.doctor_controller.get_all()
        
        for doc in doctors:
            d_id = getattr(doc, 'doctor_id', getattr(doc, 'person_id', "N/A"))
            if query and query not in doc.name.lower() and query not in doc.specialty.lower():
                continue

            status = getattr(doc, 'status', "Admitted")
            is_admitted = status == "Admitted"

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d_id), weight="bold")),
                        ft.DataCell(ft.Text(doc.name)),
                        ft.DataCell(ft.Text(doc.specialty)),
                        # Status Toggle Badge
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(status.upper(), size=10, weight="bold", color="white"),
                                bgcolor=ft.Colors.GREEN_600 if is_admitted else ft.Colors.RED_600,
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius=8,
                                on_click=lambda _, id=d_id, s=status: self.toggle_status(id, s),
                            )
                        ),
                        ft.DataCell(
                            ft.IconButton(ft.Icons.EDIT, on_click=lambda _, id=d_id: self.show_fee_dialog(id))
                        ),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Specialty")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=rows,
        )

    def build_content(self):
        self.table_container.controls = [self.create_data_table()]
        return ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Medical Staff Directory", size=28, weight="bold"),
                        ft.ElevatedButton(
                            "Add New Doctor", 
                            icon=ft.Icons.ADD, 
                            on_click=self.show_add_doctor_dialog
                        )
                    ]
                ),
                self.search_field,
                self.table_container
            ]
        )

    def build(self) -> ft.View:
        return ft.View(
            route="/doctors",
            controls=[AdminLayout(self.page, self.build_content()).build()]
        )