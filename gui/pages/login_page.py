import flet as ft

PRIMARY = ft.Colors.BLUE_600
LIGHT_BG = ft.Colors.GREY_100
CARD_BG = ft.Colors.WHITE

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.page.bgcolor = LIGHT_BG

        # UI Elements
        self.username = ft.TextField(
            hint_text="Username",
            width=320,
            filled=True,
            bgcolor=CARD_BG,
            border_radius=14,
            border_color="transparent",
            prefix_icon=ft.Icons.PERSON
        )

        self.password = ft.TextField(
            hint_text="Password",
            width=320,
            password=True,
            can_reveal_password=True,
            filled=True,
            bgcolor=CARD_BG,
            border_radius=14,
            border_color="transparent",
            prefix_icon=ft.Icons.LOCK
        )

        self.error = ft.Text(color=ft.Colors.RED_600, visible=False, size=12)

    def show_error(self, msg):
        self.error.value = msg
        self.error.visible = True
        self.page.update()

    # ---------------- Login ----------------
    def login(self, e):
        username = self.username.value.strip()
        password = self.password.value.strip()

        if not username or not password:
            self.show_error("Please enter username and password")
            return

        # Temporary authentication
        if username == "admin" and password == "admin123":
            self.page.session.set("is_logged_in", True)
            self.page.session.set("role", "admin")
            self.error.visible = False
            self.page.go("/admin-dashboard")
        elif username == "user" and password == "user123":
            self.page.session.set("is_logged_in", True)
            self.page.session.set("role", "user")
            self.error.visible = False
            self.page.go("/user-dashboard")
        else:
            self.show_error("Invalid username or password")

        self.page.update()

    def go_signup(self, e):
        self.page.go("/signup")

    # ---------------- Build ----------------
    def build(self):
        return ft.View(
            route="/",
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
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.Icon(ft.Icons.LOCK_OUTLINE, size=60, color=PRIMARY),
                                ft.Text("Welcome Back", size=22, weight=ft.FontWeight.BOLD),

                                self.username,
                                self.password,
                                self.error,

                                ft.ElevatedButton(
                                    "Login",
                                    width=320,
                                    height=45,
                                    style=ft.ButtonStyle(
                                        bgcolor=PRIMARY,
                                        color=ft.Colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=14)
                                    ),
                                    on_click=self.login
                                ),

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Don't have an account?"),
                                        ft.TextButton(
                                            "Register",
                                            on_click=self.go_signup,
                                            style=ft.ButtonStyle(color=PRIMARY)
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                )
            ]
        )
