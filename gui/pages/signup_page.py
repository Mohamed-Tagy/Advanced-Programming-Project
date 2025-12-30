import flet as ft
import re
import datetime

PRIMARY = ft.Colors.BLUE_600
LIGHT_BG = ft.Colors.GREY_100
CARD_BG = ft.Colors.WHITE

def signup_page(page: ft.Page):

    page.bgcolor = LIGHT_BG

    def field(hint, icon, password=False):
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

    username_field = field("Username", ft.Icons.PERSON)
    mobile_field = field("Mobile Number", ft.Icons.PHONE)
    email_field = field("Email Address", ft.Icons.EMAIL)
    dob_field = field("Date of Birth (YYYY-MM-DD)", ft.Icons.CALENDAR_MONTH)
    password_field = field("Password", ft.Icons.LOCK, password=True)

    gender_dropdown = ft.Dropdown(
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

    error_text = ft.Text(
        value="",
        color=ft.Colors.RED_600,
        size=12,
        visible=False
    )

    def validate(e):
        errors = []

        if not username_field.value or len(username_field.value.strip()) < 3:
            errors.append("• Username must be at least 3 characters")

        if not mobile_field.value or not mobile_field.value.isdigit() or len(mobile_field.value) < 10:
            errors.append("• Invalid mobile number")

        email_regex = r'^\S+@\S+\.\S+$'
        if not email_field.value or not re.match(email_regex, email_field.value):
            errors.append("• Invalid email address")

        if not gender_dropdown.value:
            errors.append("• Please select gender")

        try:
            dob = datetime.datetime.strptime(dob_field.value, "%Y-%m-%d").date()
            if dob > datetime.date.today():
                errors.append("• Date of birth cannot be in the future")
        except:
            errors.append("• Invalid date format")

        if not password_field.value or len(password_field.value) < 6:
            errors.append("• Password must be at least 6 characters")

        if errors:
            error_text.value = "\n".join(errors)
            error_text.visible = True
        else:
            error_text.visible = False
            page.go("/")  # بعد التسجيل يرجع Login

        page.update()

    def go_login(e):
        page.go("/")

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

                            ft.Text(
                                "Create Account",
                                size=22,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                "Fill in the details to get started",
                                size=13,
                                color=ft.Colors.GREY
                            ),

                            username_field,
                            mobile_field,
                            email_field,
                            gender_dropdown,
                            dob_field,
                            password_field,

                            error_text,

                            ft.ElevatedButton(
                                text="Sign Up",
                                width=320,
                                height=45,
                                style=ft.ButtonStyle(
                                    bgcolor=PRIMARY,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=14)
                                ),
                                on_click=validate
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
                                        on_click=go_login
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        ]
    )



