import pandas as pd

from Algorithm.Algorithm import Algorithm
from Graph.Graph import Graph


def test_graph_data():
    graph = Graph(pd.read_csv('graph-data.csv'))
    algorithm = Algorithm(graph)
    assert algorithm.get_graph().data.equals(graph.data)