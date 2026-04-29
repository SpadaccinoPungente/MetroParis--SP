from model.fermata import Fermata
from model.model import Model

model = Model()
print("Numero nodi (prima di buildGraph): ", model.get_num_nodi())
print("Numero di archi (prima di buildGraph): ", model.get_num_archi())
model.buildGraph()
print("Numero nodi (dopo buildGraph): ", model.get_num_nodi())
print("Numero di archi (dopo buildGraph): ", model.get_num_archi())

source = Fermata(2,	"Abbesses",	2.33855, 48.8843)

nodiBFS = model.getBFSNodesFromEdges(source)

print("\nN. nodi BFS: ", len(nodiBFS))
for i in range(0, 10):
    print(nodiBFS[i])

nodiDFS = model.getDFSNodesFromEdges(source)

print("\nN. nodi DFS: ", len(nodiDFS)) # la stessa di nodiBFS
for i in range(0, 10):
    print(nodiDFS[i])
# l'ordine del vettore sarà diverso invece