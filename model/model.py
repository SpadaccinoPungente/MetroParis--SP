from datetime import datetime

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}

        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f # importante per recuperare oggetto dato id!

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source) # lista di tuple
        nodiBFS = []
        for u, v in archi:
            nodiBFS.append(v)
        return nodiBFS

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi # contiene anche source, sarebbe da rimuovere

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source) # lista di tuple
        nodiDFS = []
        for u, v in archi:
            nodiDFS.append(v)
        return nodiDFS

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi # contiene anche source, sarebbe da rimuovere

    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)

        # tic = datetime.now()
        # self.add_edges1()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 1: ", toc-tic)
        #
        # tic = datetime.now()
        # self.add_edges2()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 2: ", toc-tic)

        tic = datetime.now()
        self.add_edges3()
        toc = datetime.now()
        print("Tempo impiegato da modo 3: ", toc-tic)

    # corretta ma estremamente poco efficiente
    # -> 619**2 iterazioni del doppio for
    # + query per ogni arco che aggiungiamo
    # può aver senso per grafi piccoli perché più semplice a livello di codice
    def add_edges1(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u, v):
                    self._grafo.add_edge(u, v)

    def add_edges2(self): # controllo in python (query semplice)
        self._grafo.clear_edges()
        for u in self._fermate:
            for conn in DAO.get_vicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u, v)

    def add_edges3(self): # query più complessa (no ciclo for su fermate)
        self._grafo.clear_edges()
        all_edges = DAO.getAlldges()
        for conn in all_edges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)

    def get_num_nodi(self):
        return len(self._grafo.nodes)

    def get_num_archi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate