import pandas as pd

from Heuristics.BFS import BFS
from Graphs.Graph import Graph


def test_bfs_heuristic():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = BFS(graph)
    assert bfs.calculate('Frankfurt', 'Erfurt') == 2


def test_bfs_heuristic_error():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = BFS(graph)
    try:
        bfs.calculate('Frankfurt', 'a')
    except:
        assert True
    else:
        assert False