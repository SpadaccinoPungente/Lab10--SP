import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "TdP 2025 - Lab 10"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        self._controller = None
        self._title = None
        self._txtAnno = None
        self._btnCalcola = None
        self._txt_result = None

    def load_interface(self):
        self._title = ft.Text("Country Borders", color="blue", size=24)
        self._page.controls.append(self._title)

        self._txtAnno = ft.TextField(label="Anno")
        self._btnCalcola = ft.ElevatedButton(text="Calcola Confini", on_click=self._controller.handleCalcola)
        self._page.controls.append(ft.Row([self._txtAnno, self._btnCalcola], alignment=ft.MainAxisAlignment.CENTER))

        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self._txt_result)

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller