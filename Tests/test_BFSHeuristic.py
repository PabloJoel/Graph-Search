import pandas as pd

from Heuristics.BFS import BFS
from Graphs.Graph import Graph


def test_bfs_heuristic():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = BFS(graph)
    assert bfs.calculate('Frankfurt', 'Erfurt') == 2


def test_bfs_heuristic2():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    bfs = BFS(graph)
    assert bfs.calculate('a', 'f') == 2
    assert bfs.calculate('b', 'f') == 1
    assert bfs.calculate('c', 'f') == 2
    assert bfs.calculate('d', 'f') == 1
    assert bfs.calculate('e', 'f') == float('inf')
    assert bfs.calculate('f', 'f') == 0


def test_bfs_heuristic_error():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = BFS(graph)
    assert bfs.calculate('Random', 'a') == float('inf')
    assert bfs.calculate('a', 'Random') == float('inf')
    assert bfs.calculate('a', 'a') == 0

