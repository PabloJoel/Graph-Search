import pandas as pd
from Graph.Graph import Graph


def test_data():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert data.equals(graph.data)

