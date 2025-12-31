import flet as ft
from gui.layouts.user_layout import UserLayout
from backend.controllers.doctor_controller import DoctorController
from backend.controllers.appointment_controller import AppointmentController
from backend.controllers.patient_controller import PatientController
from datetime import datetime
import threading
import time

class UserDashboard:
    def __init__(self, page: ft.Page,
                 doctor_controller: DoctorController,
                 appointment_controller: AppointmentController,
                 patient_controller: PatientController):
        self.page = page
        self.doctor_controller = doctor_controller
        self.appointment_controller = appointment_controller
        self.patient_controller = patient_controller

        # Identity
        self.user_id = self.page.session.get("user_id")
        if not self.user_id:
            self.notify("User not logged in", ft.Colors.RED)
            self.page.go("/")
        self.refresh_user_data()

        self.content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    def refresh_user_data(self):
        user = self.patient_controller.get_patient(self.user_id)
        if user:
            self.user_name = user.name
            self.page.session.set("user_name", user.name)
        else:
            self.user_name = self.page.session.get("user_name") or "Patient"

    # ---------------- Notify Function ----------------
    def notify(self, msg, color=ft.Colors.GREEN):
        sb = ft.SnackBar(
            content=ft.Text(msg, color=ft.Colors.WHITE),
            bgcolor=color,
            show_close_icon=True,
        )
        self.page.overlay.append(sb)
        sb.open = True
        self.page.update()

    
        def close_after_delay():
            time.sleep(3)
            sb.open = False
            self.page.update()

        threading.Thread(target=close_after_delay, daemon=True).start()

    def status_color(self, status):
        return {
            "Pending": ft.Colors.ORANGE,
            "Approved": ft.Colors.GREEN,
            "Scheduled": ft.Colors.BLUE_600,
            "Rejected": ft.Colors.RED,
            "Completed": ft.Colors.BLUE_GREY_400,
            "Cancelled": ft.Colors.RED_700,
        }.get(status, ft.Colors.BLACK)

    def stat_card(self, title, value, icon, color=ft.Colors.BLUE):
        return ft.Container(
            col={"sm": 12, "md": 4, "lg": 4},
            content=ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=25,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column([
                                ft.Text(title, color=ft.Colors.GREY_700, size=16),
                                ft.Text(str(value), size=32, weight="bold", color=color),
                            ], tight=True),
                            ft.Icon(icon, size=45, color=color),
                        ]
                    )
                )
            )
        )

    # ---------------- Data Fetching ----------------
    def get_doctors_list(self):
        return self.doctor_controller.get_all() or []

    def get_user_appointments(self):
        all_apps = self.appointment_controller.get_all() or []
        return [a for a in all_apps if str(a.patient_id) == str(self.user_id)]

    # ---------------- Views ----------------
    def overview_view(self):
        user_apps = self.get_user_appointments()
        doctors_count = len(self.get_doctors_list())
        appointments_count = len(user_apps)
        pending_count = len([a for a in user_apps if a.status in ["Pending", "Scheduled"]])

        notifications = []
        for app in reversed(user_apps[-3:]):
            notifications.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, size=20, color=self.status_color(app.status)),
                        ft.Text(f"Appointment #{app.appointment_id} is {app.status}", size=14)
                    ]),
                    bgcolor=ft.Colors.GREY_100, padding=10, border_radius=8
                )
            )

        return ft.Column(
            expand=True, spacing=30,
            controls=[
                ft.Text(f"Welcome back, {self.user_name}", size=28, weight="bold"),
                ft.ResponsiveRow(
                    spacing=20, run_spacing=20,
                    controls=[
                        self.stat_card("Available Doctors", doctors_count, ft.Icons.MEDICAL_SERVICES, ft.Colors.BLUE_600),
                        self.stat_card("My Appointments", appointments_count, ft.Icons.EVENT, ft.Colors.GREEN_600),
                        self.stat_card("Active Requests", pending_count, ft.Icons.PENDING, ft.Colors.ORANGE_600),
                    ]
                ),
                ft.Text("Recent Updates", size=20, weight="bold"),
                ft.Column(notifications if notifications else [ft.Text("No recent updates", color=ft.Colors.GREY_500)])
            ]
        )

    def doctors_view(self):
        def doctor_card(d):
            time_slots = [f"{h}:00" for h in range(9, 17)]
            time_dropdown = ft.Dropdown(
                label="Select Time Slot",
                options=[ft.dropdown.Option(t) for t in time_slots],
                width=240,
                bgcolor=ft.Colors.WHITE,
            )

            book_button = ft.ElevatedButton("Book Now", disabled=True)

    
            time_dropdown.on_change = lambda e: self.enable_button(book_button)

            def book(e):
                if not time_dropdown.value:
                    self.notify("Select a time slot", ft.Colors.RED)
                    return

                appointment_id = f"APP-{int(time.time())}"
                current_date = datetime.today().strftime("%Y-%m-%d")
                try:
                    self.appointment_controller.create_appointment(
                        appointment_id=appointment_id,
                        patient_id=self.user_id,
                        doctor_id=getattr(d, "doctor_id", getattr(d, "person_id", None)),
                        date=current_date,
                        time=time_dropdown.value,
                        reason="Consultation"
                    )
                    self.notify(f"Request sent to Dr. {d.name}!")
                    self.page.go("/user-appointments")
                except Exception as ex:
                    self.notify(f"Error: {str(ex)}", ft.Colors.RED)

            book_button.on_click = book

            return ft.Card(
                elevation=3,
                content=ft.Container(
                    padding=25, width=280,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON), radius=30),
                            ft.Text(f"Dr. {d.name}", size=18, weight="bold"),
                            ft.Text(d.specialty, color=ft.Colors.BLUE_700),
                            time_dropdown,
                            book_button
                        ]
                    )
                )
            )

        doctors = self.get_doctors_list()
        doctor_controls = [doctor_card(d) for d in doctors] if doctors else [
            ft.Text("No doctors available right now.", color=ft.Colors.GREY_500)
        ]

        return ft.Column(
            expand=True,
            controls=[
                ft.Text("Find a Specialist", size=28, weight="bold"),
                ft.Row(
                    wrap=True,
                    spacing=20, run_spacing=20,
                    controls=doctor_controls
                )
            ]
        )

    def enable_button(self, button: ft.ElevatedButton):
        button.disabled = False
        self.page.update()

    def appointments_view(self):
        user_apps = self.get_user_appointments()
        cards = []
        for a in user_apps:
            doc = self.doctor_controller.get_doctor(a.doctor_id)
            cards.append(
                ft.Container(
                    col={"sm": 12, "md": 6, "lg": 4},
                    content=ft.Card(
                        ft.Container(
                            padding=20,
                            content=ft.Column([
                                ft.Text(f"Ref: {a.appointment_id}", weight="bold"),
                                ft.Text(f"Doctor: Dr. {doc.name if doc else 'Specialist'}"),
                                ft.Text(f"Date: {a.date} | {a.time}"),
                                ft.Text(f"Status: {a.status}", color=self.status_color(a.status), weight="bold")
                            ])
                        )
                    )
                )
            )

        cards = cards if cards else [ft.Text("No appointments found.", color=ft.Colors.GREY_500)]
        return ft.Column(
            expand=True,
            controls=[
                ft.Text("My Appointments", size=28, weight="bold"),
                ft.ResponsiveRow(controls=cards)
            ]
        )

    def settings_view(self):
        user = self.patient_controller.get_patient(self.user_id)
        name_field = ft.TextField(label="Full Name", value=user.name if user else self.user_name)
        email_field = ft.TextField(label="Email Address", value=getattr(user, 'email', ""))
        phone_field = ft.TextField(label="Phone Number", value=getattr(user, 'phone', ""))

        def save_changes(e):
            try:
                self.patient_controller.update_patient(
                    patient_id=self.user_id,
                    name=name_field.value,
                    email=email_field.value,
                    phone=phone_field.value
                )
                self.refresh_user_data()
                self.notify("Profile saved successfully!")
                self.page.go("/user-dashboard")
            except Exception as ex:
                self.notify(f"Update failed: {str(ex)}", ft.Colors.RED)

        return ft.Column(
            expand=True, spacing=20,
            controls=[
                ft.Text("Account Settings", size=28, weight="bold"),
                ft.Container(
                    width=500, padding=20, bgcolor=ft.Colors.WHITE, border_radius=12,
                    content=ft.Column([
                        ft.Text("Edit Personal Details", size=18, weight="w500"),
                        name_field, email_field, phone_field,
                        ft.ElevatedButton(
                            "Save Changes",
                            on_click=save_changes,
                            bgcolor=ft.Colors.BLUE_700,
                            color="white"
                        )
                    ], spacing=20)
                )
            ]
        )

    # ---------------- Navigation ----------------
    def show_overview(self, e=None): self.page.go("/user-dashboard")
    def show_doctors(self, e=None): self.page.go("/user-doctors")
    def show_appointments(self, e=None): self.page.go("/user-appointments")
    def show_settings(self, e=None): self.page.go("/user-settings")

    def logout(self, e):
        self.page.session.clear()
        self.page.go("/")

    def build(self) -> ft.View:
        self.refresh_user_data()
        route = self.page.route
        if route == "/user-doctors":
            self.content_area.controls = [self.doctors_view()]
        elif route == "/user-appointments":
            self.content_area.controls = [self.appointments_view()]
        elif route == "/user-settings":
            self.content_area.controls = [self.settings_view()]
        else:
            self.content_area.controls = [self.overview_view()]

        return ft.View(
            route=route,
            bgcolor="#F8FAFC",
            padding=0,
            controls=[
                UserLayout(
                    page=self.page,
                    main_content=self.content_area,
                    current_route=route,
                    logout=self.logout,
                    overview=self.show_overview,
                    doctors=self.show_doctors,
                    appointments=self.show_appointments,
                    settings=self.show_settings
                ).build()
            ]
        )
