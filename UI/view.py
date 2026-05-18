import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        # page stuff
        self._page = page
        self._page.title = "TdP 2025 - Lab 10"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None

        # graphical elements
        self._title = None

        # definitions
        self.txtAnno = None
        self.btnCalcola = None
        self.txt_result = None
        self.ddMenuStato = None
        self.btnStatiRaggiungibili = None

    def load_interface(self):
        # title
        self._title = ft.Text("Country Borders", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW 1
        self.txtAnno = ft.TextField(label="Anno", width=250)
        self.btnCalcola = ft.ElevatedButton(
            text="Calcola Confini",
            on_click=self._controller.handleCalcola,
            width=250
        )

        row1 = ft.Row([self.txtAnno, self.btnCalcola], alignment=ft.MainAxisAlignment.CENTER)

        # ROW 2
        self.ddMenuStato = ft.Dropdown(label="Stato di partenza", on_change=self._controller.choiceDDStatoPartenza, width=250)
        self.btnStatiRaggiungibili = ft.ElevatedButton(
            text="Calcola Stati Raggiungibili",
            on_click=self._controller.handleStatiRaggiungibili,
            width=250
        )

        row2 = ft.Row([self.ddMenuStato, self.btnStatiRaggiungibili], alignment=ft.MainAxisAlignment.CENTER)

        # List View where the results are displayed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.extend([row1, row2, self.txt_result])

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()