import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCalcola(self, e):
        try: anno = int(self._view._txtAnno)
        except ValueError: self._view.create_alert("Inserire un valore numerico.")

        if not 1816 <= anno <= 2016:
            self._view.create_alert("Inserire un anno compreso tra il 1816 e il 2016!")
            return

        self._model.buildGraph(anno)

        nodes_w_deg = self._model.getNodesWDeg()

        self._view.controls.clear()

        self._view.txt._txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getLenConnComps()} componenti connesse."))

        for node, deg in nodes_w_deg:
            self._view.txt._txt_result.controls.append(ft.Text(f"{node}, {deg} stati confinanti."))

        self._view.update_page()


