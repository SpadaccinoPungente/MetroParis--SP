import flet as ft
import os

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Metro Paris 2025"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200  # window's width is 200 px
        page.window_height = 800
        page.window_center()
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self.lst_result = None
        self.title = None
        self.logo = None
        self.ddStazArrivo = None
        self.ddStazPartenza = None
        self.btnCrea = None
        self.btnCreaGrafoPesato = None
        self.btnCreaMultiGrafo = None
        self.btnCreaGrafoCamminiMinimi = None
        self.btnCalcolaDijkstraPath = None

    def load_interface(self):
        # title
        self.title = ft.Text("Metro Paris", color="green", size=24)

        # ROW with title
        img_path = os.path.join(os.getcwd(), 'database/RATP.png')
        self.logo = ft.Image(src=img_path,
                              width=100,
                              height=100,
                              )

        row1 = ft.Row([self.title, self.logo],
                      alignment=ft.MainAxisAlignment.CENTER)

        # Row with controls
        self.btnCrea = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self.ddStazPartenza = ft.Dropdown(label="Stazione di Partenza")
        self.ddStazArrivo = ft.Dropdown(label="Stazione di Arrivo")
        self.btnCalcola = ft.ElevatedButton(text="Calcola Raggiungibili", on_click=self._controller.handleCercaRaggiungibili)

        # Load elements in DD
        self._controller.loadFermate(self.ddStazPartenza)
        self._controller.loadFermate(self.ddStazArrivo)

        row2 = ft.Row([self.btnCrea,
                       self.ddStazPartenza,
                       self.ddStazArrivo,
                       self.btnCalcola,
                       ], alignment=ft.MainAxisAlignment.CENTER, spacing=30)

        # Additional row
        self.btnCreaGrafoPesato = ft.ElevatedButton(text="Crea Grafo Pesato", on_click=self._controller.handleCreaGrafoPesato)

        self.btnCreaMultiGrafo = ft.ElevatedButton(text="Crea Multi-Grafo", on_click=self._controller.handleCreaMultiGrafo)

        self.btnCreaGrafoCamminiMinimi = ft.ElevatedButton(text="Crea Grafo cammini minimi", on_click=self._controller.handleCalcolaDijkstraPath)

        self.btnCalcolaDijkstraPath = ft.ElevatedButton(text="Calcola Dijkstra", on_click=self._controller.handleCreaGrafoCamminiMinimi)

        row3 = ft.Row(
            [self.btnCreaGrafoPesato, self.btnCreaMultiGrafo, self.btnCreaGrafoCamminiMinimi, self.btnCalcolaDijkstraPath],
            alignment=ft.MainAxisAlignment.CENTER, spacing=30
        )

        # Row with listview
        self.lst_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

        self._page.add(row1, row2, row3, self.lst_result)

    def update_page(self):
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