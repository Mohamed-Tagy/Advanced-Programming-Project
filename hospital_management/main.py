import flet as ft

from utils.config import APP_TITLE
from utils.db_utils import Database
# from gui.login_page import LoginPage


class HospitalApp:
   

    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()
        self.configure_page()
        self.show_login()

    def configure_page(self):
        
        self.page.title = APP_TITLE
        self.page.window_width = 900
        self.page.window_height = 600
        self.page.window_resizable = False
        self.page.theme_mode = ft.ThemeMode.LIGHT

    def clear_page(self):
        
        self.page.controls.clear()
        self.page.update()

    def show_login(self):
       
        self.clear_page()
        login_page = LoginPage(self.page, self)
        self.page.add(login_page.build())
        self.page.update()


def main(page: ft.Page):
   
    HospitalApp(page)


if __name__ == "__main__":
    ft.app(target=main)
