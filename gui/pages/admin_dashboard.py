import flet as ft
from gui.layouts.admin_layout import AdminLayout
from backend.controllers.appointment_controller import AppointmentController
from backend.controllers.admin_controller import AdminController

class AdminDashboard:
    def __init__(self, page: ft.Page, 
                 appointment_controller: AppointmentController,
                 admin_controller: AdminController):
        self.page = page
        self.appointment_controller = appointment_controller
        self.admin_controller = admin_controller

    def stat_card(self, title, value, icon, color):
        return ft.Container(
            col={"sm": 12, "md": 4},
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "black")),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column([
                        ft.Text(title, size=14, color=ft.Colors.GREY_700, weight="w500"),
                        ft.Text(str(value), size=30, weight="bold", color=ft.Colors.BLACK),
                    ], spacing=5),
                    ft.Icon(icon, color=color, size=35),
                ]
            ),
        )

    def show_add_admin_dialog(self, e):
        """Logic to create a new Admin via the AdminController."""
        name_ref = ft.Ref[ft.TextField]()
        id_ref = ft.Ref[ft.TextField]()
        gender_ref = ft.Ref[ft.Dropdown]()
        dob_ref = ft.Ref[ft.TextField]() 

        def save_admin(e):
            if not name_ref.current.value or not id_ref.current.value:
                self.page.snack_bar = ft.SnackBar(ft.Text("ID and Name are required!"))
                self.page.snack_bar.open = True
                self.page.update()
                return

            try:
                self.admin_controller.create_admin(
                    admin_id=id_ref.current.value.strip(),
                    name=name_ref.current.value.strip(),
                    gender=gender_ref.current.value or "Not Specified",
                    dob=None 
                )
                
                dlg.open = False
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Admin {id_ref.current.value} Added Successfully!"), 
                    bgcolor="green"
                )
                self.page.snack_bar.open = True
                self.page.update()
                
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Add New Administrator"),
            content=ft.Column([
                ft.TextField(ref=id_ref, label="Admin ID (e.g., ADM01)"),
                ft.TextField(ref=name_ref, label="Full Name"),
                ft.Dropdown(
                    ref=gender_ref,
                    label="Gender",
                    options=[
                        ft.dropdown.Option("Male"),
                        ft.dropdown.Option("Female"),
                    ]
                )
            ], tight=True, spacing=10, width=400),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.page.close(dlg)),
                ft.ElevatedButton("Save", on_click=save_admin, bgcolor=ft.Colors.BLUE_700, color="white")
            ],
        )
        self.page.open(dlg)

    def build_content(self):
        appointments = self.appointment_controller.get_all()

        pending = len([a for a in appointments if a.status in ["Scheduled", "Pending"]])
        completed = len([a for a in appointments if a.status == "Completed"])
        cancelled = len([a for a in appointments if a.status in ["Cancelled", "Rejected"]])

        recent_requests_list = []
        recent_items = appointments[-5:] if len(appointments) >= 5 else appointments
        
        for a in reversed(recent_items):
            status_color = {
                "Scheduled": ft.Colors.ORANGE,
                "Pending": ft.Colors.ORANGE,
                "Completed": ft.Colors.GREEN,
                "Cancelled": ft.Colors.RED,
                "Rejected": ft.Colors.RED,
            }.get(a.status, ft.Colors.GREY)

            recent_requests_list.append(
                ft.Container(
                    padding=10,
                    border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_100)),
                    content=ft.Row([
                        ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.BLUE_700),
                        ft.Column([
                            ft.Text(f"Patient ID: {a.patient_id}", weight="bold", size=14),
                            ft.Text(f"Schedule: {a.date} at {a.time}", size=12, color=ft.Colors.GREY_600),
                        ], expand=True),
                        ft.Chip(
                            label=ft.Text(a.status, size=11, color="white"),
                            bgcolor=status_color,
                            shape=ft.RoundedRectangleBorder(radius=5),
                        )
                    ])
                )
            )

        return ft.Column(
            expand=True,
            spacing=30,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Row([
                    ft.Column([
                        ft.Text("Admin Overview", size=28, weight="bold"),
                        ft.Text("Hospital performance at a glance", color=ft.Colors.GREY_600),
                    ]),
                    ft.ElevatedButton(
                        "Add Admin", 
                        icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                        bgcolor=ft.Colors.BLUE_700,
                        color="white",
                        on_click=self.show_add_admin_dialog
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.ResponsiveRow(
                    spacing=20,
                    controls=[
                        self.stat_card("Active Bookings", pending, ft.Icons.PENDING_ACTIONS, ft.Colors.ORANGE),
                        self.stat_card("Total Treated", completed, ft.Icons.CHECK_CIRCLE_OUTLINE, ft.Colors.GREEN),
                        self.stat_card("Cancellations", cancelled, ft.Icons.REPORT_GMAILERRORRED, ft.Colors.RED),
                    ],
                ),

                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    padding=25,
                    border_radius=15,
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.HISTORY, color=ft.Colors.BLUE_GREY),
                            ft.Text("Recent Appointment Activities", size=18, weight="bold"),
                        ], spacing=10),
                        ft.Divider(height=20, color=ft.Colors.GREY_100),
                        *(recent_requests_list if recent_requests_list else [ft.Text("No recent activity found.")])
                    ], spacing=10)
                ),
            ],
        )

    def build(self) -> ft.View:
        return ft.View(
            route="/admin-dashboard",
            padding=0,
            bgcolor="#F4F6F8",
            controls=[AdminLayout(self.page, self.build_content()).build()]
        )