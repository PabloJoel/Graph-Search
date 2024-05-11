import pandas as pd

from Graphs.PandasGraph import PandasGraph
from Algorithms.MOA import MOA
from Tests.heuristics import MockedHeuristicMOA

# Creación de un grafo a partir de un csv
data = pd.read_csv('moa-data.csv')
graph = PandasGraph(
    data=data,
    bidirectional=False,
    weight_cols=['weight_1', 'weight_2']
)

# Creación de un algoritmo a partir de un grafo y una heurística
moa = MOA(graph, heuristic=MockedHeuristicMOA(graph))

# Ejecución del algoritmo
moa.run(start_vertex='s', end_vertices=['y1','y2','y3'])

# Extracción de métricas
metrics = moa.metrics
print(metrics)

# Extracción de las soluciones
min_cost = moa.solution.get_min_solution_cost('s')
print('Min cost solution:', min_cost)