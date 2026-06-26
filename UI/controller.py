import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCalcola(self, e):
        try:
            anno = int(self._view._txtAnno.value)
        except ValueError:
            self._view.create_alert("Inserire un valore numerico.")
            return

        if not 1816 <= anno <= 2016:
            self._view.create_alert("Inserire un anno compreso tra il 1816 e il 2016!")
            return

        self._model.buildGraph(anno)

        nodes_w_deg = self._model.getNodesWDeg()

        nodes_w_deg_sorted = sorted(nodes_w_deg, key=lambda node: node[0].StateNme)

        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getLenConnComps()} componenti connesse."))

        for node, deg in nodes_w_deg_sorted:
            self._view._txt_result.controls.append(ft.Text(f"{node}, stati confinanti: {deg}."))

        countries = sorted([c for c in self._model.id_map_countries.values()], key=lambda c: c.StateNme)
        self._view._ddCountry.options = [ft.dropdown.Option(key=c.CCode, text=c.StateNme) for c in countries]
        self._view.update_page()

    def handleRaggiungibili(self, e):
        selected_id = self._view._ddCountry.value

        if not selected_id:
            self._view.create_alert("Selezionare uno stato!")
            return

        selected_country = self._model.id_map_countries.get(int(selected_id))

        reachable = self._model.getReachableStates2(selected_country)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stati raggiungibili da {selected_country.StateNme}:"))

        for country in sorted(reachable, key=lambda c: c.StateNme):
            self._view._txt_result.controls.append(ft.Text(f"- {country}"))

        self._view.update_page()


