import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self.graph = nx.Graph()
        self.id_map_countries = {c.CCode: c for c in DAO.getAllCountries()}

    def buildGraph(self, anno):
        self.graph.clear()
        edges_by_id = DAO.getAllEdges(anno)
        for idu, idv in edges_by_id:
            u = self.id_map_countries[idu]
            v = self.id_map_countries[idv]
            self.graph.add_edge(u, v)

    def getNodesWDeg(self):
        result = []
        for node in self.graph.nodes():
            deg = self.graph.degree(node)
            result.append((node, deg))
        return result

    def getLenConnComps(self):
        return len(list(nx.connected_components(self.graph)))