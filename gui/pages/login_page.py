import flet as ft

PRIMARY = ft.Colors.BLUE_600
LIGHT_BG = ft.Colors.GREY_100
CARD_BG = ft.Colors.WHITE

class LoginPage:
    def __init__(self, page: ft.Page, auth_ctrl):
        self.page = page
        self.auth_ctrl = auth_ctrl 
        
        self.username = ft.TextField(
            label="User ID", width=320, filled=True, bgcolor=CARD_BG,
            border_radius=14, prefix_icon=ft.Icons.PERSON_OUTLINED
        )
        self.password = ft.TextField(
            label="Password", width=320, password=True, can_reveal_password=True,
            filled=True, bgcolor=CARD_BG, border_radius=14, prefix_icon=ft.Icons.LOCK_OUTLINED
        )
        self.error = ft.Text(color=ft.Colors.RED_600, visible=False, size=12, weight="bold")
        self.loader = ft.ProgressBar(width=320, color=PRIMARY, visible=False)

    def login(self, e):
        user_id = self.username.value.strip()
        password = self.password.value.strip()

        if not user_id or not password:
            self.show_error("Please enter credentials")
            return

        self.error.visible = False
        self.loader.visible = True
        self.page.update()

        result = self.auth_ctrl.login(user_id, password)

        if result:
            self.page.session.set("is_logged_in", True)
            self.page.session.set("user_id", result["user"].person_id)
            self.page.session.set("user_name", result["user"].name)
            self.page.session.set("role", result["role"])
            self.page.go(result["route"])
        else:
            self.show_error("Invalid ID. User not found.")

    def show_error(self, msg):
        self.error.value = msg
        self.error.visible = True
        self.loader.visible = False
        self.page.update()

    def build(self):
        return ft.View(
            route="/",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=LIGHT_BG,
            controls=[
                ft.Container(
                    width=400, padding=40, bgcolor=CARD_BG, border_radius=24,
                    shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.BLACK12),
                    content=ft.Column(
                        horizontal_alignment="center", spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.LOCAL_HOSPITAL_ROUNDED, size=50, color=PRIMARY),
                            ft.Text("Hospital Management", size=24, weight="bold"),
                            self.username, self.password, self.loader, self.error,
                            ft.ElevatedButton("Login", width=320, height=50, bgcolor=PRIMARY, color="white", on_click=self.login),
                            ft.TextButton("Register New Account", on_click=lambda _: self.page.go("/signup"))
                        ]
                    )
                )
            ]
        )