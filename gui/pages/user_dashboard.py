import flet as ft
from gui.layouts.user_layout import UserLayout

class UserDashboard:
    def __init__(self, page: ft.Page):
        self.page = page

        # -------- Temporary Data --------
        self.doctors = [
            {"name": "Dr. Khaled", "specialty": "Cardiology", "slots": ["10:00", "11:00", "12:00"]},
            {"name": "Dr. Mona", "specialty": "Dermatology", "slots": ["12:00", "13:00", "14:00"]},
            {"name": "Dr. Ahmed", "specialty": "Pediatrics", "slots": ["09:00", "10:00"]},
        ]
        self.appointments = []

        self.content = ft.Column(expand=True)

    # Utilities
    def notify(self, msg, color=ft.Colors.GREEN):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def status_color(self, status):
        return {"Pending": ft.Colors.ORANGE, "Approved": ft.Colors.GREEN, "Rejected": ft.Colors.RED}.get(status, ft.Colors.BLACK)

    def stat_card(self, title, value, icon, color=ft.Colors.BLUE):
        return ft.Container(
            col=4,
            content=ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=20,
                    content=ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Column([
                                ft.Text(title, color=ft.Colors.GREY),
                                ft.Text(str(value), size=28, weight="bold", color=color),
                            ]),
                            ft.Icon(icon, size=40, color=color),
                        ]
                    )
                )
            )
        )

    # Views
    def overview_view(self):
        return ft.Column(
            expand=True,
            spacing=25,
            controls=[
                ft.Text("User Overview", size=26, weight="bold"),
                ft.Column(
                    spacing=20,
                    controls=[
                        self.stat_card("Doctors", len(self.doctors), ft.Icons.MEDICAL_SERVICES),
                        self.stat_card("Appointments", len(self.appointments), ft.Icons.EVENT),
                        self.stat_card(
                            "Pending",
                            len([a for a in self.appointments if a["status"] == "Pending"]),
                            ft.Icons.PENDING
                        ),
                    ]
                ),
            ]
        )

    def doctors_view(self):
        def doctor_card(d):
            time_dropdown = ft.Dropdown(
                label="Available Times",
                options=[ft.dropdown.Option(t) for t in d["slots"]],
                width=220,
            )
            def book(e):
                if not time_dropdown.value:
                    self.notify("Please select a time", ft.Colors.RED)
                    return
                self.appointments.append({
                    "doctor": d["name"],
                    "specialty": d["specialty"],
                    "time": time_dropdown.value,
                    "status": "Pending"
                })
                d["slots"].remove(time_dropdown.value)
                self.notify(f"Appointment booked with {d['name']} at {time_dropdown.value}")
                self.show_appointments()

            return ft.Card(
                elevation=3,
                content=ft.Container(
                    padding=30,
                    width=280,
                    content=ft.Column(
                        spacing=18,
                        controls=[
                            ft.Text(d["name"], size=22, weight="bold"),
                            ft.Text(d["specialty"], color=ft.Colors.GREY, size=17),
                            time_dropdown,
                            ft.ElevatedButton("Book Appointment", icon=ft.Icons.EVENT, on_click=book)
                        ]
                    )
                )
            )

        return ft.Column(
            expand=True,
            spacing=20,
            scroll="adaptive",
            controls=[
                ft.Text("Doctors", size=26, weight="bold"),
                ft.Row(
                    spacing=25,
                    run_spacing=25,
                    wrap=True,
                    controls=[doctor_card(d) for d in self.doctors]
                )
            ]
        )

    def appointments_view(self):
        return ft.Column(
            expand=True,
            scroll="adaptive",
            spacing=15,
            controls=[
                ft.Text("Appointments", size=26, weight="bold"),
                *[
                    ft.Card(
                        ft.Container(
                            padding=12,
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    self._row("Doctor:", a["doctor"]),
                                    self._row("Specialty:", a.get("specialty", "")),
                                    self._row("Time:", a["time"]),
                                    self._row("Status:", a["status"], color=self.status_color(a["status"]), bold=True)
                                ]
                            )
                        )
                    ) for a in self.appointments
                ]
            ]
        )

    def _row(self, label, value, color=None, bold=False):
        return ft.Row(
            spacing=10,
            controls=[
                ft.Text(label, weight="bold"),
                ft.Text(value, color=color, weight="bold" if bold else None)
            ]
        )

    # Navigation
    def show_overview(self, e=None):
        self.content.controls = [self.overview_view()]
        self.page.update()

    def show_doctors(self, e=None):
        self.content.controls = [self.doctors_view()]
        self.page.update()

    def show_appointments(self, e=None):
        self.content.controls = [self.appointments_view()]
        self.page.update()

    def logout(self, e):
        self.page.session.clear()
        self.page.go("/")

    # Build
    def build(self) -> ft.View:
        self.show_overview()
        return ft.View(
            route="/user-dashboard",
            bgcolor=ft.Colors.GREY_100,
            controls=[
                UserLayout(
                    page=self.page,
                    main_content=self.content,
                    logout=self.logout,
                    overview=self.show_overview,
                    doctors=self.show_doctors,
                    appointments=self.show_appointments
                ).build()
            ]
        )
