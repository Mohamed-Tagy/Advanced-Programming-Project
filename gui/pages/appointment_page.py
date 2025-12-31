import flet as ft
from gui.layouts.admin_layout import AdminLayout
from backend.controllers.appointment_controller import AppointmentController
import time

class AppointmentPage:
    def __init__(self, page: ft.Page, appointment_controller: AppointmentController):
        self.page = page
        self.appointment_controller = appointment_controller
        
        self.search_field = ft.TextField(
            label="Search by Patient, Doctor, or ID", 
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.update_table,
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
        self.table_container = ft.Column(scroll=ft.ScrollMode.AUTO)

    def get_status_color(self, status):
        return {
            "Completed": ft.Colors.GREEN_600,
            "Pending": ft.Colors.ORANGE_700,
            "Cancelled": ft.Colors.RED_600,
            "No Show": ft.Colors.BLUE_GREY_600,
            "Scheduled": ft.Colors.BLUE_600,
            "Approved": ft.Colors.GREEN_600,
        }.get(status, ft.Colors.GREY_400)

    def toggle_appointment_status(self, appointment_id, current_status):
        """Cycles status: Scheduled -> Pending -> Completed -> No Show -> Cancelled"""
        status_order = ["Scheduled", "Pending", "Completed", "No Show", "Cancelled"]
        try:
            current_index = status_order.index(current_status) if current_status in status_order else 0
            new_status = status_order[(current_index + 1) % len(status_order)]
            
            self.appointment_controller.update_appointment_status(appointment_id, new_status)
            
            self.update_table()
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Appointment updated to {new_status}"))
            self.page.snack_bar.open = True
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"), bgcolor="red")
            self.page.snack_bar.open = True
        self.page.update()

    def handle_action(self, action_type, appointment_id):
        try:
            status_map = {"cancel": "Cancelled", "complete": "Completed", "no_show": "No Show"}
            new_status = status_map.get(action_type)
            if new_status:
                self.appointment_controller.update_appointment_status(appointment_id, new_status)
            
            self.update_table()
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Success: {new_status}"), bgcolor=ft.Colors.GREEN_700)
            self.page.snack_bar.open = True
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"), bgcolor=ft.Colors.RED_700)
            self.page.snack_bar.open = True
        self.page.update()

    def update_table(self, e=None):
        self.table_container.controls = [self.create_data_table()]
        self.page.update()

    def create_data_table(self):
        rows = []
        search_query = self.search_field.value.lower() if self.search_field.value else ""
        appointments = self.appointment_controller.get_all()
        
        for appt in appointments:
            if search_query:
                match = (search_query in str(appt.appointment_id).lower() or 
                         search_query in str(appt.patient_id).lower() or
                         search_query in str(appt.doctor_id).lower())
                if not match: continue

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(appt.appointment_id), weight="bold")),
                        ft.DataCell(ft.Text(str(appt.patient_id))),
                        ft.DataCell(ft.Text(str(appt.doctor_id))),
                        ft.DataCell(ft.Text(f"{appt.date} {appt.time}")),
                        # --- MODIFIED: Clickable Chip to change status ---
                        ft.DataCell(
                            ft.Chip(
                                label=ft.Text(appt.status, color="white", size=11, weight="bold"),
                                bgcolor=self.get_status_color(appt.status),
                                shape=ft.RoundedRectangleBorder(radius=5),
                                on_click=lambda _, id=appt.appointment_id, s=appt.status: self.toggle_appointment_status(id, s)
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(text="Complete", icon=ft.Icons.CHECK_CIRCLE, on_click=lambda _, id=appt.appointment_id: self.handle_action("complete", id)),
                                        ft.PopupMenuItem(text="No Show", icon=ft.Icons.DO_NOT_DISTURB_ALT, on_click=lambda _, id=appt.appointment_id: self.handle_action("no_show", id)),
                                        ft.PopupMenuItem(text="Cancel", icon=ft.Icons.CANCEL, on_click=lambda _, id=appt.appointment_id: self.handle_action("cancel", id)),
                                    ]
                                )
                            ])
                        ),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Patient")),
                ft.DataColumn(ft.Text("Doctor")),
                ft.DataColumn(ft.Text("Date/Time")),
                ft.DataColumn(ft.Text("Status (Click to toggle)")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=rows,
            column_spacing=45,
            heading_row_color=ft.Colors.GREY_100,
            expand=True
        )

    def show_add_appointment_dialog(self, e):
        patient_ref = ft.Ref[ft.TextField]()
        doctor_ref = ft.Ref[ft.TextField]()
        date_ref = ft.Ref[ft.TextField]()
        time_ref = ft.Ref[ft.TextField]()

        def save_appt(e):
            if not patient_ref.current.value or not doctor_ref.current.value:
                return
            try:
                new_id = f"APP-{int(time.time())}"
                self.appointment_controller.create_appointment(
                    appointment_id=new_id,
                    patient_id=patient_ref.current.value,
                    doctor_id=doctor_ref.current.value,
                    date=date_ref.current.value or "2025-01-01",
                    time=time_ref.current.value or "10:00",
                    reason="Admin Manual Entry"
                )
                dlg.open = False
                self.update_table()
                self.page.update()
            except Exception as ex:
                print(f"Error: {ex}")

        dlg = ft.AlertDialog(
            title=ft.Text("Schedule New Appointment"),
            content=ft.Column([
                ft.TextField(ref=patient_ref, label="Patient ID"),
                ft.TextField(ref=doctor_ref, label="Doctor ID"),
                ft.Row([
                    ft.TextField(ref=date_ref, label="Date", value="2025-01-01", expand=1),
                    ft.TextField(ref=time_ref, label="Time", value="10:00", expand=1),
                ])
            ], tight=True, spacing=10, width=400),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.close_dlg(dlg)),
                ft.ElevatedButton("Create", on_click=save_appt, bgcolor=ft.Colors.BLUE_700, color="white")
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def close_dlg(self, dlg):
        dlg.open = False
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
                            ft.Text("Appointment Registry", size=28, weight="bold"),
                            ft.Text("Monitor and update hospital schedules", color=ft.Colors.GREY_600),
                        ]),
                        ft.ElevatedButton("New Appointment", icon=ft.Icons.ADD, on_click=self.show_add_appointment_dialog)
                    ]
                ),
                self.search_field,
                self.table_container
            ]
        )

    def build(self) -> ft.View:
        return ft.View(
            route="/appointments",
            controls=[AdminLayout(self.page, self.build_content()).build()]
        )