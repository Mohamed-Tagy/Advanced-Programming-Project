import flet as ft
import datetime

PRIMARY = ft.Colors.BLUE_600
CARD_BG = ft.Colors.WHITE
LIGHT_BG = ft.Colors.GREY_100

class SignupPage:
    def __init__(self, page: ft.Page, auth_ctrl):
        self.page = page
        self.auth_ctrl = auth_ctrl
        self.selected_dob = None

        self.dob_display = ft.Text("Not Selected", color=ft.Colors.GREY_700)
        self.error_text = ft.Text(color=ft.Colors.RED_600, size=12, visible=False, weight="bold")
        self.loader = ft.ProgressBar(width=320, color=PRIMARY, visible=False)

        self.username_field = self._field("Username (ID)", ft.Icons.PERSON_OUTLINED)
        self.fullname_field = self._field("Full Name", ft.Icons.BADGE_OUTLINED)
        self.mobile_field = self._field("Mobile Number", ft.Icons.PHONE_OUTLINED)
        self.email_field = self._field("Email Address", ft.Icons.EMAIL_OUTLINED)
        self.password_field = self._field("Password", ft.Icons.LOCK_OUTLINED, password=True)
        
        self.gender_dropdown = ft.Dropdown(
            width=320, label="Gender", filled=True, bgcolor=CARD_BG, border_radius=14,
            options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")]
        )

        self.role_dropdown = ft.Dropdown(
            width=320, label="Register As", filled=True, bgcolor=CARD_BG, border_radius=14,
            value="Patient", 
            options=[
                ft.dropdown.Option("Patient"), 
                ft.dropdown.Option("Admin")
            ]
        )

        self.date_picker = ft.DatePicker(
            on_change=self.handle_date_change,
            first_date=datetime.datetime(1920, 1, 1),
            last_date=datetime.datetime.now(),
        )
        if self.date_picker not in self.page.overlay:
            self.page.overlay.append(self.date_picker)

    def _field(self, label, icon, password=False):
        return ft.TextField(
            label=label, width=320, password=password, can_reveal_password=password,
            filled=True, bgcolor=CARD_BG, border_radius=14, prefix_icon=icon
        )

    def open_date_picker(self, e):
        self.date_picker.open = True
        self.page.update()

    def handle_date_change(self, e):
        if self.date_picker.value:
            self.selected_dob = self.date_picker.value.date()
            self.dob_display.value = self.selected_dob.strftime("%Y-%m-%d")
            self.dob_display.color = ft.Colors.BLACK
            self.page.update()

    def validate_and_submit(self, e):
        data = {
            "user_id": self.username_field.value.strip(),
            "full_name": self.fullname_field.value.strip(),
            "phone": self.mobile_field.value.strip(),
            "email": self.email_field.value.strip(),
            "gender": self.gender_dropdown.value,
            "dob": self.selected_dob,
            "password": self.password_field.value,
            "role": self.role_dropdown.value 
        }

        if not all([data["user_id"], data["full_name"], data["gender"], data["dob"], data["password"]]):
            self.error_text.value = "• Please fill in all required fields"
            self.error_text.visible = True
            self.page.update()
            return

        self.error_text.visible = False
        self.loader.visible = True
        self.page.update()

        try:
            if data["role"] == "Admin":
                self.auth_ctrl.register_admin(data)
            else:
                self.auth_ctrl.register_patient(data)
            
            self.page.snack_bar = ft.SnackBar(ft.Text(f"{data['role']} Registered!"), bgcolor="green")
            self.page.snack_bar.open = True
            self.page.go("/") 
            
        except Exception as ex:
            self.error_text.value = f"• {str(ex)}"
            self.error_text.visible = True
            self.loader.visible = False
            self.page.update()

    def build(self) -> ft.View:
        return ft.View(
            route="/signup",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=LIGHT_BG,
            controls=[
                ft.Container(
                    width=400, padding=30, bgcolor=CARD_BG, border_radius=25,
                    shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.BLACK12),
                    content=ft.Column(
                        horizontal_alignment="center", spacing=12,
                        controls=[
                            ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, size=50, color=PRIMARY),
                            ft.Text("Account Registration", size=24, weight="bold"),
                            
                            self.role_dropdown, 
                            self.username_field, 
                            self.fullname_field, 
                            self.mobile_field,
                            self.email_field, 
                            self.gender_dropdown,
                            
                            ft.Container(
                                width=320, padding=12, bgcolor=ft.Colors.GREY_50, 
                                border_radius=12, border=ft.border.all(1, ft.Colors.GREY_200),
                                content=ft.Row([
                                    ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREY_600),
                                    self.dob_display,
                                    ft.TextButton("Select DOB", on_click=self.open_date_picker)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            ),
                            
                            self.password_field, 
                            self.loader, 
                            self.error_text,
                            
                            ft.ElevatedButton(
                                "Create Account", width=320, height=50, bgcolor=PRIMARY, 
                                color="white", on_click=self.validate_and_submit,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14))
                            ),
                            ft.TextButton("Back to Login", on_click=lambda _: self.page.go("/"))
                        ]
                    )
                )
            ]
        )