import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.countries = DAO.get_all_countries()
        self.id_map_stati = {c.CCode: c for c in self.countries}

    def build_graph(self, year):
        self.grafo.clear()
        edges = DAO.get_borders(year, self.id_map_stati)
        for u, v in edges: self.grafo.add_edge(u, v) # Nodi aggiunti in automatico

    def get_num_connected_components(self):
        return nx.number_connected_components(self.grafo)

    def get_nodes_degrees(self):
        # Ordiniamo i nodi usando il nome dello stato come chiave
        nodi_ordinati = sorted(self.grafo.nodes(), key=lambda x: x.StateNme)
        return [(n, self.grafo.degree(n)) for n in nodi_ordinati]

    # Implementazione 1 (iterativa)
    def get_reachable_states_iterative(self, start_node):
        visitati = []
        da_visitare = [start_node]  # Inizializzazione con lo stato scelto

        while da_visitare:  # Continua finché la lista da visitare non è vuota
            corrente = da_visitare.pop(0)  # Estrazione del primo nodo (approccio FIFO)

            if corrente not in visitati:
                visitati.append(corrente)  # Inserimento nei visitati

                # Esplorazione dei vicini
                for vicino in self.grafo.neighbors(corrente):
                    if vicino not in visitati and vicino not in da_visitare:
                        da_visitare.append(vicino)

        # Rimuoviamo il nodo iniziale per restituire solo i nodi *raggiungibili da esso*
        if start_node in visitati:
            visitati.remove(start_node)
        return visitati

    # Implementazione 2 (ricorsiva)
    def get_reachable_states_recursive(self, start_node):
        visitati = set()  # Usiamo un set per un controllo di esistenza immediato

        # Funzione ricorsiva interna (funzione di supporto)
        def dfs(nodo):
            visitati.add(nodo)  # Segna il nodo corrente come visitato

            # Ricorsione sui vicini non ancora visitati
            for vicino in self.grafo.neighbors(nodo):
                if vicino not in visitati:
                    dfs(vicino)

        # Avviamo la ricorsione dal nodo di partenza
        dfs(start_node)

        # Trasformiamo in lista e rimuoviamo il nodo di partenza
        risultato = list(visitati)
        if start_node in risultato: risultato.remove(start_node)
        return risultato

    # Implementazione 3 (con bfs_tree)
    def get_reachable_states_nx_tree(self, start_node):
        # Genera un sotto-albero orientato che rappresenta la visita in ampiezza (BFS)
        albero_visita = nx.bfs_tree(self.grafo, source=start_node)
        # I nodi dell'albero corrispondono esattamente a tutti i nodi visitati
        risultato = list(albero_visita.nodes())
        if start_node in risultato: risultato.remove(start_node)
        return risultato

    # Implementazione 4 (con node_connected_component)
    def get_reachable_states_nx_component(self, start_node):
        # Restituisce direttamente il set di nodi della componente connessa associata
        componente = nx.node_connected_component(self.grafo, start_node)
        risultato = list(componente)
        if start_node in risultato: risultato.remove(start_node)
        return risultato
