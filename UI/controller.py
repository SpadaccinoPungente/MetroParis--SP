from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self._fermataPartenza = None
        self._fermataArrivo = None

    def handleCreaGrafo(self, e):
        ti = datetime.now()
        self._model.buildGraph3()
        n_nodes, n_edges = self._model.getGraphDetails()
        if not n_nodes:
            self._view.lst_result.controls.append(ft.Text("Errore nella creazione del grafo.", color="red"))
            return
        self._view.lst_result.controls.append(
            ft.Text(f"Grafo creato con buildGraph3! {n_nodes} nodi e {n_edges} archi."
                    f"\nTime elapsed: {datetime.now()-ti} s",
                    color="green")
        )
        self._view.update_page()

        # ti = datetime.now()
        # self._model.buildGraph2()
        # n_nodes, n_edges = self._model.getGraphDetails()
        # if not n_nodes:
        #     self._view.lst_result.controls.append(ft.Text("Errore nella creazione del grafo.", color="red"))
        #     return
        # self._view.lst_result.controls.append(
        #     ft.Text(f"Grafo creato con buildGraph2! {n_nodes} nodi e {n_edges} archi."
        #             f"\nTime elapsed: {datetime.now()-ti} s",
        #             color="green")
        # )
        # self._view.update_page()

        # ti = datetime.now()
        # self._model.buildGraph1()
        # n_nodes, n_edges = self._model.getGraphDetails()
        # if not n_nodes:
        #     self._view.lst_result.controls.append(ft.Text("Errore nella creazione del grafo.", color="red"))
        #     return
        # self._view.lst_result.controls.append(
        #     ft.Text(f"Grafo creato con buildGraph1! {n_nodes} nodi e {n_edges} archi."
        #             f"\nTime elapsed: {datetime.now()-ti} s",
        #             color="green")
        # )
        # self._view.update_page()

    def handleCercaRaggiungibili(self, e):
        if self._fermataPartenza is None:
            self._view.create_alert("Selezionare stazione di partenza!")
            return

        nodi_raggiungibili_bfs = self._model.getNodiRaggiungibiliBFS(self._fermataPartenza)

        nodi_raggiungibili_dfs = self._model.getNodiRaggiungibiliDFS(self._fermataPartenza)

        self._view.lst_result.controls.clear()

        self._view.lst_result.controls.append(ft.Text(f"Nodi raggiungibili da {self._fermataPartenza} con BFS:"))
        for n in nodi_raggiungibili_bfs: self._view.lst_result.controls.append(ft.Text(n))

        self._view.lst_result.controls.append(ft.Text(f"Nodi raggiungibili da {self._fermataPartenza} con DFS:"))
        for n in nodi_raggiungibili_dfs: self._view.lst_result.controls.append(ft.Text(n))

        self._view.update_page()

    def handleCreaGrafoPesato(self, e):
        self._model.buildWeightedGraph()
        n_nodes, n_edges = self._model.getGraphDetails()
        if not n_nodes:
            self._view.lst_result.controls.append(ft.Text("Errore nella creazione del grafo.", color="red"))
            return
        self._view.lst_result.controls.append(
            ft.Text(f"Grafo pesato creato correttamente! {n_nodes} nodi e {n_edges} archi.", color="green")
        )
        self._view.update_page()

    def handleCreaMultiGrafo(self, e):
        self._model.buildMultiGraph()
        n_nodes, n_edges = self._model.getMultiGraphDetails()
        if not n_nodes:
            self._view.lst_result.controls.append(ft.Text("Errore nella creazione del grafo.", color="red"))
            return
        self._view.lst_result.controls.append(
            ft.Text(f"Multi-grafo creato correttamente! {n_nodes} nodi e {n_edges} archi.", color="green")
        )
        self._view.update_page()

    def handleCreaGrafoCamminiMinimi(self, e):
        self._model.buildGraphCamminiMinimi()
        n_nodes, n_edges = self._model.getGraphCamminiMinimiDetails()
        if not n_nodes:
            self._view.lst_result.controls.append(ft.Text("Errore nella creazione del grafo.", color="red"))
            return
        self._view.lst_result.controls.append(
            ft.Text(f"Grafo per i cammini minimi creato correttamente! {n_nodes} nodi e {n_edges} archi.", color="green")
        )
        self._view.btnCalcolaDijkstraPath.disabled = False
        self._view.update_page()

    def handleCalcolaDijkstraPath(self, e):
        if self._fermataPartenza is None or self._fermataArrivo is None:
            self._view.create_alert("Selezionare stazione di partenza e di arrivo!")
            return

        self._view.lst_result.controls.clear()

        tempo_totale, cammino_nodi = self._model.getDijkstraPath(self._fermataPartenza, self._fermataArrivo)

        if tempo_totale is None or not cammino_nodi:
            self._view.lst_result.controls.append(
                ft.Text(f"Nessun percorso trovato tra {self._fermataPartenza.nome} e {self._fermataArrivo.nome}.",
                        color="red")
            )
            self._view.update_page()
            return

        self._view.lst_result.controls.append(
            ft.Text(f"Cammino ottimo trovato! Tempo di percorrenza: {tempo_totale*60}' attraverso i seguenti nodi:")
        )
        for n in cammino_nodi: self._view.lst_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

        self._view.update_page()

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None: self._fermataPartenza = None
        else: self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None: self._fermataArrivo = None
        else: self._fermataArrivo = e.control.data
