import pandas as pd

from Graphs.PandasGraph import PandasGraph
from Algorithms.AStar import AStar
from Tests.heuristics import MockedHeuristicMOA

# Creación de un grafo a partir de un csv
data = pd.read_csv('moa-data.csv')
graph = PandasGraph(
    data=data,
    source_col='source',
    target_col='target',
    bidirectional=False,
    weight_cols=['weight_1', 'weight_2']
)

# Creación de un algoritmo a partir de un grafo y una heurística
moa = AStar(graph, heuristic=MockedHeuristicMOA(graph))

# Ejecución del algoritmo
moa.run(start_vertex='a', end_vertex='f', show_by_step=True, show_end=True)

# Extracción de métricas
metrics = moa.metrics

# Extracción de las soluciones
solutions = moa.solution
min_cost = moa.solution.get_min_solution_cost()
