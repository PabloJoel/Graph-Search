import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph


def test_graph_data():
    graph = Graph(pd.read_csv('graph-data.csv'))
    algorithm = Algorithm(graph, None)
    assert algorithm.graph.data.equals(graph.data)