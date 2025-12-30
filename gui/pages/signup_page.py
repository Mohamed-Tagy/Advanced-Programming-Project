import flet as ft
import re
import datetime

PRIMARY = ft.Colors.BLUE_600
LIGHT_BG = ft.Colors.GREY_100
CARD_BG = ft.Colors.WHITE

class SignupPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = LIGHT_BG

        # -------- Fields --------
        self.username_field = self._field("Username", ft.Icons.PERSON)
        self.mobile_field = self._field("Mobile Number", ft.Icons.PHONE)
        self.email_field = self._field("Email Address", ft.Icons.EMAIL)
        self.dob_field = self._field("Date of Birth (YYYY-MM-DD)", ft.Icons.CALENDAR_MONTH)
        self.password_field = self._field("Password", ft.Icons.LOCK, password=True)

        self.gender_dropdown = ft.Dropdown(
            width=320,
            hint_text="Gender",
            filled=True,
            bgcolor=CARD_BG,
            border_radius=14,
            border_color="transparent",
            options=[
                ft.dropdown.Option("Male"),
                ft.dropdown.Option("Female"),
            ]
        )

        self.error_text = ft.Text(
            value="",
            color=ft.Colors.RED_600,
            size=12,
            visible=False
        )

    # -------- Reusable Field --------
    def _field(self, hint, icon, password=False):
        return ft.TextField(
            hint_text=hint,
            width=320,
            password=password,
            can_reveal_password=password,
            filled=True,
            bgcolor=CARD_BG,
            border_radius=14,
            border_color="transparent",
            prefix_icon=icon
        )

    # -------- Validation Logic --------
    def validate(self, e):
        errors = []

        if not self.username_field.value or len(self.username_field.value.strip()) < 3:
            errors.append("• Username must be at least 3 characters")

        if not self.mobile_field.value or not self.mobile_field.value.isdigit() or len(self.mobile_field.value) < 10:
            errors.append("• Invalid mobile number")

        email_regex = r'^\S+@\S+\.\S+$'
        if not self.email_field.value or not re.match(email_regex, self.email_field.value):
            errors.append("• Invalid email address")

        if not self.gender_dropdown.value:
            errors.append("• Please select gender")

        try:
            dob = datetime.datetime.strptime(self.dob_field.value, "%Y-%m-%d").date()
            if dob > datetime.date.today():
                errors.append("• Date of birth cannot be in the future")
        except:
            errors.append("• Invalid date format (YYYY-MM-DD)")

        if not self.password_field.value or len(self.password_field.value) < 6:
            errors.append("• Password must be at least 6 characters")

        if errors:
            self.error_text.value = "\n".join(errors)
            self.error_text.visible = True
        else:
            self.error_text.visible = False

            # 🔌 Backend integration will go here later
            # Example: user_service.register_user(...)

            # Optional: log the user in automatically after signup
            # self.page.session.set("is_logged_in", True)
            # self.page.session.set("role", "user")

            self.page.go("/")  # back to login

        self.page.update()

    def go_login(self, e):
        self.page.go("/")

    # -------- Build View --------
    def build(self) -> ft.View:
        return ft.View(
            route="/signup",
            appbar=None,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Container(
                        width=380,
                        padding=30,
                        bgcolor=CARD_BG,
                        border_radius=20,
                        shadow=ft.BoxShadow(
                            color=ft.Colors.BLACK12,
                            blur_radius=20,
                            offset=ft.Offset(0, 10)
                        ),
                        content=ft.Column(
                            spacing=18,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.PERSON_ADD_ALT_1,
                                    size=60,
                                    color=PRIMARY
                                ),
                                ft.Text("Create Account", size=22, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    "Fill in the details to get started",
                                    size=13,
                                    color=ft.Colors.GREY
                                ),

                                self.username_field,
                                self.mobile_field,
                                self.email_field,
                                self.gender_dropdown,
                                self.dob_field,
                                self.password_field,

                                self.error_text,

                                ft.ElevatedButton(
                                    text="Sign Up",
                                    width=320,
                                    height=45,
                                    style=ft.ButtonStyle(
                                        bgcolor=PRIMARY,
                                        color=ft.Colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=14)
                                    ),
                                    on_click=self.validate
                                ),

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=5,
                                    controls=[
                                        ft.Text(
                                            "Do you already have an account?",
                                            size=13,
                                            color=ft.Colors.GREY_700
                                        ),
                                        ft.TextButton(
                                            content=ft.Text(
                                                "Login",
                                                weight=ft.FontWeight.BOLD,
                                                color=PRIMARY
                                            ),
                                            on_click=self.go_login
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                )
            ]
        )
