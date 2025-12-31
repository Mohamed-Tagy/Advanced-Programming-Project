import flet as ft
from gui.layouts.admin_layout import AdminLayout
from backend.controllers.patient_controller import PatientController
from datetime import datetime
import time

class PatientsPage:
    def __init__(self, page: ft.Page, patient_controller: PatientController):
        self.page = page
        self.patient_controller = patient_controller
        self.search_field = ft.TextField(
            label="Search by Name or ID",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.update_table,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
        self.table_container = ft.Column(scroll=ft.ScrollMode.AUTO)

    def update_table(self, e=None):
        """Refreshes the data table content."""
        self.table_container.controls = [self.create_data_table()]
        self.page.update()

    def handle_status_change(self, action, pid):
        """Executes Admit/Discharge and updates the UI."""
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            if action == "admit":
                self.patient_controller.admit_patient(pid, admission_date=today, doctor_id="STAFF-01")
            else:
                self.patient_controller.discharge_patient(pid, discharge_date=today)
            
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Patient {pid} {action}ted successfully."), 
                bgcolor=ft.Colors.GREEN_700 if action == "admit" else ft.Colors.BLUE_700
            )
            self.page.snack_bar.open = True
            
            self.update_table() 
            
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()

    def create_data_table(self):
        rows = []
        search_query = self.search_field.value.lower() if self.search_field.value else ""
        patients = self.patient_controller.get_all()
        
        for patient in patients:
            p_id = getattr(patient, 'patient_id', getattr(patient, 'person_id', "N/A"))
            
            if search_query and search_query not in patient.name.lower() and search_query not in str(p_id).lower():
                continue

            is_admitted = getattr(patient, 'admitted', 0) == 1
            status_text = "INPATIENT" if is_admitted else "OUTPATIENT"
            status_color = ft.Colors.GREEN_600 if is_admitted else ft.Colors.BLUE_GREY_400
            status_icon = ft.Icons.BED if is_admitted else ft.Icons.PERSON_OUTLINED

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p_id), weight="bold")),
                        ft.DataCell(ft.Text(patient.name)),
                        ft.DataCell(ft.Text(str(patient.age))),
                        ft.DataCell(ft.Text(patient.gender)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(status_icon, size=16, color=status_color),
                                    ft.Text(status_text, size=12, weight="bold", color=status_color)
                                ], spacing=5),
                                padding=ft.padding.all(5),
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.LOGIN, 
                                    tooltip="Admit Patient", 
                                    icon_color=ft.Colors.GREEN,
                                    visible=not is_admitted,
                                    on_click=lambda _, pid=p_id: self.handle_status_change("admit", pid)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.LOGOUT, 
                                    tooltip="Discharge Patient", 
                                    icon_color=ft.Colors.RED_400,
                                    visible=is_admitted,
                                    on_click=lambda _, pid=p_id: self.handle_status_change("discharge", pid)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_NOTE, 
                                    tooltip="Add Medical Note", 
                                    on_click=lambda _, pid=p_id: self.show_note_dialog(pid)
                                ),
                            ])
                        ),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Age")),
                ft.DataColumn(ft.Text("Gender")),
                ft.DataColumn(ft.Text("Current Status")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=rows,
            column_spacing=35,
            heading_row_color=ft.Colors.GREY_100,
        )

    
    def show_register_dialog(self, e):
        name_ref = ft.Ref[ft.TextField]()
        age_ref = ft.Ref[ft.TextField]()
        gender_ref = ft.Ref[ft.Dropdown]()

        def save_patient(_):
            if not name_ref.current.value: return
            try:
                new_id = f"PAT-{int(time.time())}"
                self.patient_controller.create_patient(
                    patient_id=new_id,
                    name=name_ref.current.value,
                    age=int(age_ref.current.value or 0),
                    gender=gender_ref.current.value
                )
                self.page.dialog.open = False
                self.update_table()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("New Patient Registration"),
            content=ft.Column([
                ft.TextField(ref=name_ref, label="Full Name"),
                ft.TextField(ref=age_ref, label="Age", keyboard_type=ft.KeyboardType.NUMBER),
                ft.Dropdown(ref=gender_ref, label="Gender", options=[
                    ft.dropdown.Option("Male"), ft.dropdown.Option("Female")
                ]),
            ], tight=True),
            actions=[ft.TextButton("Cancel", on_click=lambda _: self.close_dialog()),
                     ft.ElevatedButton("Register", on_click=save_patient)]
        )
        self.page.dialog.open = True
        self.page.update()

    def show_note_dialog(self, pid):
        note_input = ft.TextField(label="Clinical Note", multiline=True, min_lines=3)
        def save_note(_):
            self.patient_controller.add_medical_note(pid, note_input.value)
            self.page.dialog.open = False
            self.update_table()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Medical Record: {pid}"),
            content=note_input,
            actions=[ft.TextButton("Close", on_click=lambda _: self.close_dialog()),
                     ft.ElevatedButton("Save Note", on_click=save_note)]
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def build_content(self):
        self.table_container.controls = [self.create_data_table()]
        return ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Text("Patient Registry", size=28, weight="bold"),
                            ft.Text("Manage Inpatient/Outpatient status", color=ft.Colors.GREY_600),
                        ]),
                        ft.ElevatedButton("Register Patient", icon=ft.Icons.PERSON_ADD, on_click=self.show_register_dialog)
                    ]
                ),
                ft.Container(bgcolor=ft.Colors.WHITE, padding=15, border_radius=10, content=ft.Row([self.search_field])),
                ft.Container(bgcolor=ft.Colors.WHITE, padding=10, border_radius=10, expand=True, content=self.table_container)
            ]
        )

    def build(self) -> ft.View:
        return ft.View(route="/patients", controls=[AdminLayout(self.page, self.build_content()).build()])