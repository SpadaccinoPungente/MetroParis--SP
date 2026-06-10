import math

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._id_map_fermate = {f.id_fermata: f for f in DAO.getAllFermate()}
        self._graph = nx.DiGraph()
        self._multiGraph = nx.MultiDiGraph()
        self._graphCamminiMinimi = nx.DiGraph()

    """
    Si sperimentino tre diverse modalità di costruzione degli archi del grafo: 
    1. doppio loop sulle coppie di vertici, per ogni coppia fare una query per 
    determinare se esiste l'arco o meno 
    2. singolo loop sui vertici, per ogni vertice fare una query che restituisca l'elenco di 
    tutti i vertici che dovranno essere adiacenti 
    3. nessun loop, singola query che produce "subito" tutto il grafo. 
    """

    def buildGraph1(self):
        # Come prima cosa sempre pulire il grafo e inizializzare i nodi
        self._graph.clear()
        self._graph.add_nodes_from(self._id_map_fermate.values()) # .values() per avere i valori del dizionario

        for id1 in self._id_map_fermate:
            for id2 in self._id_map_fermate:
                if id1 != id2 and DAO.existsEdge(self._id_map_fermate[id1], self._id_map_fermate[id2]):
                    # Passiamo gli oggetti Fermata al DAO
                    self._graph.add_edge(self._id_map_fermate[id1], self._id_map_fermate[id2])

    def buildGraph2(self):
        self._graph.clear()
        self._graph.add_nodes_from(self._id_map_fermate.values())

        for id_nodo in self._id_map_fermate:
            id_nbrs = DAO.getNeighbors(self._id_map_fermate[id_nodo]) # ritorna una lista con tutte le stazioni raggiungibili
            for id_nbr in id_nbrs:
                nbr = self._id_map_fermate.get(id_nbr)
                if nbr: self._graph.add_edge(self._id_map_fermate[id_nodo], nbr) # meglio controllare che nbr sia valido

    def buildGraph3(self):
        self._graph.clear()
        self._graph.add_nodes_from(self._id_map_fermate.values())

        archi_by_id = DAO.getAllEdges()
        archi_w_data = [
            (self._id_map_fermate[e[0]], self._id_map_fermate[e[1]])
            for e in archi_by_id
            if e[0] in self._id_map_fermate and e[1] in self._id_map_fermate
        ]
        # Se nel database della tabella connessione ci fosse un ID stazione vecchio o errato che non è presente nella tabella
        # fermata, self._id_map_fermate.get() restituirebbe None. In quel caso, inseriresti nel grafo una tupla del tipo:
        # (None, OggettoFermata), che farebbe arrabbiare NetworkX.

        self._graph.add_edges_from(archi_w_data)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getNodiRaggiungibiliBFS(self, source):
        # bfs_edges si propaga come un'onda concentrica analizzando prima tutti i vicini, poi i vicini dei vicini e così via.
        # restituisce l'elenco degli archi visitati in ordine cronologico (bisogna recuperare i vertici)
        archi_raggiungibili = nx.bfs_edges(self._graph, source)
        nodi_raggiungibili = [v for _, v in archi_raggiungibili]
        return [source] + nodi_raggiungibili # bfs_edges non include l'origine

    def getNodiRaggiungibiliDFS(self, source):
        # dfs_edges si propaga in profondità lungo i rami del grafo.
        # Anche questo non include l'origine e restituisce le coppie (u, v).
        archi_raggiungibili = nx.dfs_edges(self._graph, source)
        nodi_raggiungibili = [v for _, v in archi_raggiungibili]
        return [source] + nodi_raggiungibili # se scrivessi [source] dopo sarebbe l'ultima, così è la prima

    def buildWeightedGraph(self):
        self._graph.clear()
        self._graph.add_nodes_from(self._id_map_fermate.values())

        weighted_edges_by_id = DAO.getEdgesWithWeight()

        weighed_edges_w_data = [
            (self._id_map_fermate[e[0]], self._id_map_fermate[e[1]], {"weight": e[2]})
            for e in weighted_edges_by_id
            if e[0] in self._id_map_fermate and e[1] in self._id_map_fermate  # Controllo di sicurezza opzionale
        ]

        self._graph.add_edges_from(weighed_edges_w_data)

    def buildMultiGraph(self):
        self._multiGraph.clear()
        self._multiGraph.add_nodes_from(self._id_map_fermate.values())

        # Recuperiamo l'elenco dal DAO con le velocità delle linee
        connessioni_dict = DAO.getEdgesWithVelocity()
        archi_w_data = []

        for c in connessioni_dict:
            f_partenza = self._id_map_fermate.get(c['id_stazP'])
            f_arrivo = self._id_map_fermate.get(c['id_stazA'])
            velocita = c['velocita']

            if f_partenza and f_arrivo and velocita > 0:
                # 1. Calcolo della distanza in linea d'aria (Euclidea)
                distanza = math.sqrt(
                    (f_arrivo.coordX - f_partenza.coordX)**2 +(f_arrivo.coordY - f_partenza.coordY)**2
                )

                # 2. Calcolo del tempo di percorrenza (Peso)
                tempo = distanza / velocita

                # 3. Struttura per il multigrafo pesato
                archi_w_data.append((f_partenza, f_arrivo, {"weight": tempo}))

        self._multiGraph.add_edges_from(archi_w_data)

    def getMultiGraphDetails(self):
        return self._multiGraph.number_of_nodes(), self._multiGraph.number_of_edges()

    """
    lunghezza = nx.dijkstra_path_length(G, source, target, weight='weight')
    
    cammino = nx.dijkstra_path(G, source, target, weight='weight')
    
    lunghezza, cammino = nx.single_source_dijkstra(G, source, target, weight='weight')
    """

    def buildGraphCamminiMinimi(self):
        self._graphCamminiMinimi.clear()
        self._graphCamminiMinimi.add_nodes_from(self._id_map_fermate.values())

        archi_dict = DAO.getEdgesWithMaxVelocity()
        archi_w_data = []

        for a in archi_dict:
            f_partenza = self._id_map_fermate.get(a['id_stazP'])
            f_arrivo = self._id_map_fermate.get(a['id_stazA'])
            velocita = a['vel_max']

            if f_partenza and f_arrivo and velocita > 0:
                distanza = math.sqrt(
                    (f_arrivo.coordX - f_partenza.coordX)**2 +(f_arrivo.coordY - f_partenza.coordY)**2
                )
                archi_w_data.append((f_partenza, f_arrivo, {"weight": distanza / velocita}))

        self._graphCamminiMinimi.add_edges_from(archi_w_data)

    def getGraphCamminiMinimiDetails(self):
        return self._graphCamminiMinimi.number_of_nodes(), self._graphCamminiMinimi.number_of_edges()

    def getDijkstraPath(self, partenza, arrivo):
        try:
            tempo_totale, cammino_nodi = nx.single_source_dijkstra(
                self._graphCamminiMinimi, source=partenza, target=arrivo, weight='weight'
            )
            return tempo_totale, cammino_nodi
        except nx.NetworkXNoPath:
            return None, []