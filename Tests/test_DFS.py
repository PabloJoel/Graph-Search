import pandas as pd

from Graphs.Graph import Graph
from Algorithms.DFS import DFS
from Visualizers.DashVisualizer import DashVisualizer


def test_data_bidirectional():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data, bidirectional=True)
    bfs = DFS(graph)
    bfs.run(1, end_vertex=3, show_end=True)

    expected = pd.DataFrame([
        {'source':1, 'target':2},
        {'source':2, 'target':3},
    ])

    assert bfs.solution.data.equals(expected)


def test_data():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    bfs = DFS(graph)
    bfs.run(1, show_end=True)

    assert bfs.solution.data.equals(data)


def test_data_bidirectional_dash():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data, bidirectional=True)
    bfs = DFS(graph, visualizer=DashVisualizer())
    bfs.run(1, end_vertex=3, show_end=True)

    expected = pd.DataFrame([
        {'source':1, 'target':2},
        {'source':2, 'target':3}
    ])

    assert bfs.solution.data.equals(expected)


def test_data_dash():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    bfs = DFS(graph, visualizer=DashVisualizer())
    bfs.run(1,show_end=True)

    assert bfs.solution.data.equals(data)
