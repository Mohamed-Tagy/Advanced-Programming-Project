import flet as ft

PRIMARY = ft.Colors.BLUE_600
LIGHT_BG = ft.Colors.GREY_100
CARD_BG = ft.Colors.WHITE

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}

def login_page(page: ft.Page):
    page.bgcolor = LIGHT_BG

    username = ft.TextField(
        hint_text="Username",
        width=320,
        filled=True,
        bgcolor=CARD_BG,
        border_radius=14,
        border_color="transparent",
        prefix_icon=ft.Icons.PERSON
    )

    password = ft.TextField(
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

    error = ft.Text(color=ft.Colors.RED_600, visible=False, size=12)

    def show_error(msg):
        error.value = msg
        error.visible = True
        page.update()

    def login(e):
        u = username.value.strip()
        p = password.value.strip()

        if not u or not p:
            show_error("Please enter username and password")
            return

        if u not in USERS or USERS[u]["password"] != p:
            show_error("Invalid username or password")
            return

        role = USERS[u]["role"]

        page.session.set("is_logged_in", True)
        page.session.set("role", role)
        page.session.set("username", u)

        if role == "admin":
            page.go("/admin-dashboard")
        else:
            page.go("/user-dashboard")

    def go_signup(e):
        page.go("/signup")

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

                            username,
                            password,
                            error,

                            ft.ElevatedButton(
                                "Login",
                                width=320,
                                height=45,
                                style=ft.ButtonStyle(
                                    bgcolor=PRIMARY,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=14)
                                ),
                                on_click=login
                            ),

                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Text("Don't have an account?"),
                                    ft.TextButton(
                                        "Register",
                                        on_click=go_signup,
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
