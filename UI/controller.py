import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCalcola(self, e):
        anno_str = self._view.txtAnno.value

        try:
            anno = int(anno_str)
            if anno < 1816 or anno > 2016:
                self._view.txt_result.controls.append(
                    ft.Text(value="Inserire un anno compreso tra 1816 e 2016.",
                            color='orange'))
                self._view.update_page()
                return
        except ValueError:
            self._view.txt_result.controls.append(
                ft.Text(value="Errore: inserire un numero intero valido.",
                        color='red'))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text("Sto creando il grafo..."))
        self._model.build_graph(anno)

        # Esercizio 1
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(value="Grafo correttamente creato!",
                    color='green'))

        # Punto D: numero componenti connesse
        n_comp = self._model.get_num_connected_components()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {n_comp} componenti connesse."))

        # Punto C: elenco stati + grado
        self._view.txt_result.controls.append(ft.Text("Di seguito il dettaglio sui nodi:"))
        for nodo, grado in self._model.get_nodes_degrees():
            self._view.txt_result.controls.append(ft.Text(f"{nodo.StateNme} -- {grado} vicini."))

        self._view.update_page()