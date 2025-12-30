import flet as ft
from gui.layouts.user_layout import user_layout

def user_dashboard(page: ft.Page):

    # ---------------- Data ----------------
    doctors = [
        {"name": "Dr. Khaled", "specialty": "Cardiology", "slots": ["10:00", "11:00", "12:00"]},
        {"name": "Dr. Mona", "specialty": "Dermatology", "slots": ["12:00", "13:00", "14:00"]},
        {"name": "Dr. Ahmed", "specialty": "Pediatrics", "slots": ["09:00", "10:00"]},
    ]
    appointments = []

    # ---------------- Helpers ----------------
    def notify(msg, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def status_color(status):
        return {
            "Pending": ft.Colors.ORANGE,
            "Approved": ft.Colors.GREEN,
            "Rejected": ft.Colors.RED,
        }.get(status, ft.Colors.BLACK)

    def stat_card(title, value, icon, color=ft.Colors.BLUE):
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

    # ---------------- Views ----------------
    def overview_view():
        return ft.Column(
            expand=True,
            spacing=25,
            controls=[
                ft.Text("User Overview", size=26, weight="bold"),
                ft.Column(
                    spacing=20,
                    controls=[
                        stat_card("Doctors", len(doctors), ft.Icons.MEDICAL_SERVICES),
                        stat_card("Appointments", len(appointments), ft.Icons.EVENT),
                        stat_card("Pending", len([a for a in appointments if a["status"]=="Pending"]), ft.Icons.PENDING),
                    ]
                ),
            ]
        )

    # ---------- Doctors View ----------
    def doctors_view():

        def doctor_card(d):
            time_dropdown = ft.Dropdown(
                label="Available Times",
                options=[ft.dropdown.Option(t) for t in d["slots"]],
                width=220,  # أكبر شوي
            )

            def book(e):
                if not time_dropdown.value:
                    notify("Please select a time", ft.Colors.RED)
                    return

                appointments.append({"doctor": d["name"], "specialty": d["specialty"], "time": time_dropdown.value, "status": "Pending"})
                d["slots"].remove(time_dropdown.value)
                notify(f"Appointment booked with {d['name']} at {time_dropdown.value}")
                show_appointments()

            return ft.Card(
                elevation=3,
                content=ft.Container(
                    padding=30,  # زيادة مساحة padding
                    width=280,   # كبرت مساحة الكارت
                    content=ft.Column(
                        spacing=18,  # زيادة المسافة بين العناصر
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
            scroll="adaptive",  # scroll تلقائي لو الكاردات كثيرة
            controls=[
                ft.Text("Doctors", size=26, weight="bold"),
                ft.Row(
                    spacing=25,
                    run_spacing=25,
                    wrap=True,
                    controls=[doctor_card(d) for d in doctors]
                )
            ]
        )

    # ---------- Appointments View ----------
    def appointments_view():
        return ft.Column(
            expand=True,
            scroll="adaptive",  # scroll تلقائي
            spacing=15,
            controls=[
                ft.Text("Appointments", size=26, weight="bold"),
                *[
                    ft.Card(
                        ft.Container(
                            padding=12,  # أقل padding لتقليل المساحات الفارغة
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Text("Doctor:", weight="bold"),
                                            ft.Text(a["doctor"])
                                        ]
                                    ),
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Text("Specialty:", weight="bold"),
                                            ft.Text(a.get("specialty", ""))
                                        ]
                                    ),
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Text("Time:", weight="bold"),
                                            ft.Text(a["time"])
                                        ]
                                    ),
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Text("Status:", weight="bold"),
                                            ft.Text(a["status"], color=status_color(a["status"]), weight="bold")
                                        ]
                                    )
                                ]
                            )
                        )
                    )
                    for a in appointments
                ]
            ]
        )

    # ---------------- Dynamic Content ----------------
    content = ft.Column(expand=True)

    def show_overview(e=None):
        content.controls = [overview_view()]
        page.update()

    def show_doctors(e=None):
        content.controls = [doctors_view()]
        page.update()

    def show_appointments(e=None):
        content.controls = [appointments_view()]
        page.update()

    def logout(e):
        page.session.clear()
        page.go("/")

    show_overview()

    return ft.View(
        "/user-dashboard",
        bgcolor=ft.Colors.GREY_100,
        controls=[
            user_layout(
                page,
                main_content=content,
                logout=logout,
                overview=show_overview,
                doctors=show_doctors,
                appointments=show_appointments,
            )
        ]
    )
