import flet as ft
from gui.styles.colors import PRIMARY, BACKGROUND

def app_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY,
            background=BACKGROUND,
        )
    )

