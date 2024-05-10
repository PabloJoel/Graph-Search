import pandas as pd

from Graphs.PandasGraph import PandasGraph

# Creación de un grafo a partir de un csv
data = pd.read_csv('astar-data.csv')
graph1 = PandasGraph(
    data=data,
    source_col='source',
    target_col='target',
    bidirectional=False,
    weight_cols=['weight_1']
)


# Creación de un grafo bidireccional a partir de un csv
data = pd.read_csv('astar-data.csv')
graph2 = PandasGraph(
    data=data,
    source_col='source',
    target_col='target',
    bidirectional=True,
    weight_cols=['weight_1']
)


# Creación de un grafo con múltiples pesos a partir de un csv
data = pd.read_csv('biobjective-data.csv')
graph3 = PandasGraph(
    data=data,
    source_col='source',
    target_col='target',
    bidirectional=False,
    weight_cols=['weight_1', 'weight_2']
)


# Creación del Visualizer y visualización de los grafos
from Visualizers.DashVisualizer import DashVisualizer
#visualizer = DashVisualizer()
#visualizer.show(graph1)
#visualizer.show(graph2)
#visualizer.show(graph3)

# Extracción de métricas tras la ejecución del algoritmo
from Algorithms.Dijkstra import Dijkstra
dijkstra = Dijkstra(graph=graph1)
dijkstra.run(start_vertex='a', end_vertex='f')
print(dijkstra.metrics)


# Creación del algoritmo BDijkstra para resolver el problema con dos pesos
from Algorithms.BDijkstra import BDijkstra
#bdijkstra = BDijkstra(graph=graph3, visualizer=DashVisualizer())
#bdijkstra.run(start_vertex='a', end_vertex='f', show_by_step=True, show_end=True)


# Creación del algoritmo MOA* para resolver el problema con dos pesos
#from Algorithms.MOA import MOA
#from Tests.heuristics import MockedHeuristicAutomatic
#moa = MOA(graph=graph3, visualizer=DashVisualizer(), heuristic=MockedHeuristicAutomatic(graph3, 'f'))
#moa.run(start_vertex='a', end_vertices=['f'], show_end=True)



