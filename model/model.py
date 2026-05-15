import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.countries = DAO.get_all_countries()
        self.id_map = {c.CCode: c for c in self.countries}

    def build_graph(self, year):
        self.grafo.clear()
        edges = DAO.get_borders(year, self.id_map)
        for u, v in edges: self.grafo.add_edge(u, v) # Nodi aggiunti in automatico

    def get_num_connected_components(self):
        return nx.number_connected_components(self.grafo)

    def get_nodes_degrees(self):
        # Ritorna una lista di tuple (Nodo, Grado)
        return [(n, self.grafo.degree(n)) for n in self.grafo.nodes()]