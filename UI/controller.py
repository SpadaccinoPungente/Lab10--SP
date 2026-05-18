import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self.choiceStatoPartenza = None

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

        self._fillDDStatiRaggiungibili()

    def handleStatiRaggiungibili(self, e):
        # Controllo di sicurezza iniziale
        if self.choiceStatoPartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: selezionare uno stato.", color="red"))
            self._view.update_page()
            return

        # Conversione in intero per id_map_stati
        stato_partenza = self._model.id_map_stati[int(self.choiceStatoPartenza)]

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Analisi e confronto per lo stato: {stato_partenza.StateNme}\n", weight="bold", size=16)
        )

        # Iterativo (BFS)
        start_time = time.time()
        res_iter = self._model.get_reachable_states_iterative(stato_partenza)
        time_iter = time.time() - start_time

        # 2. Ricorsione (DFS)
        start_time = time.time()
        res_ric = self._model.get_reachable_states_recursive(stato_partenza)
        time_ric = time.time() - start_time

        # 3. nx.bfs_tree
        start_time = time.time()
        res_tree = self._model.get_reachable_states_nx_tree(stato_partenza)
        time_tree = time.time() - start_time

        # 4. nx.node_connected_component
        start_time = time.time()
        res_comp = self._model.get_reachable_states_nx_component(stato_partenza)
        time_comp = time.time() - start_time

        # Ordiniamo l'output alfabeticamente (usiamo res_iter come riferimento)
        raggiungibili_ordinati = sorted(res_iter, key=lambda x: x.StateNme)

        # Stampa confronto tempi
        self._view.txt_result.controls.append(ft.Text("[CONFRONTO TEMPI DI ESECUZIONE]", color="blue"))
        self._view.txt_result.controls.append(
            ft.Text(f"1. Iterativo (BFS): {time_iter:.6f} secondi (Nodi: {len(res_iter)})", color="blue")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"2. Ricorsivo (DFS): {time_ric:.6f} secondi (Nodi: {len(res_ric)})", color="blue")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"3. NX Albero (nx.bfs_tree): {time_tree:.6f} secondi (Nodi: {len(res_tree)})", color="blue")
        )
        self._view.txt_result.controls.append(
            ft.Text(
                f"4. NX Componente (nx.node_connected_component): {time_comp:.6f} secondi (Nodi: {len(res_comp)})", color="blue")
        )

        # Stampa stati
        self._view.txt_result.controls.append(ft.Text(f"\nStati raggiungibili da {stato_partenza.StateNme}:"))

        for stato in raggiungibili_ordinati: self._view.txt_result.controls.append(ft.Text(f"{stato.StateNme}"))

        self._view.update_page()

    def _fillDDStatiRaggiungibili(self):
        """
        Popola il Dropdown menu esclusivamente con i nodi che fanno parte del grafo appena calcolato nell'Esercizio 1.
        """
        self._view.ddMenuStato.options.clear()

        # Estraggo i nodi correnti del grafo e li ordino alfabeticamente
        nodi_grafo = sorted(self._model.grafo.nodes(), key=lambda x: x.StateNme)

        """
        # Modo 1 (for)
        for nodo in nodi_grafo:
            self._view.ddMenuStato.options.append(ft.dropdown.Option(key=str(nodo.CCode), text=nodo.StateNme))

        # Modo 2 (map)
        opzioni = map(lambda nodo: ft.dropdown.Option(key=str(nodo.CCode), text=nodo.StateNme), nodi_grafo)
        self._view.ddMenuStato.options = opzioni
        """

        # Modo 3 (list comprehension)
        self._view.ddMenuStato.options = [ft.dropdown.Option(key=str(nodo.CCode), text=nodo.StateNme) for nodo in nodi_grafo]

        self._view.update_page()

    def choiceDDStatoPartenza(self, e):
        """
        Gestore dell'evento on_change del Dropdown (se si desidera tracciare la scelta in tempo reale in una variabile d'istanza).
        """
        self.choiceStatoPartenza = e.control.data