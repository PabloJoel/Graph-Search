import pandas as pd

from Graphs.Graph import Graph
from Algorithms.BFS import BFS
from Visualizers.DashVisualizer import DashVisualizer


def test_data_bidirectional():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt')
    bfs.show()

    expected = pd.DataFrame(data=[
        {'source': 'Frankfurt', 'target': 'Mannheim', 'weight_1':85},
        {'source': 'Frankfurt', 'target': 'Würzburg', 'weight_1':217},
        {'source': 'Frankfurt', 'target': 'Kassel', 'weight_1':173},
        {'source': 'Mannheim', 'target': 'Karlsruhe', 'weight_1':80},
        {'source': 'Würzburg', 'target': 'Erfurt', 'weight_1':186},
        {'source': 'Würzburg', 'target': 'Nürnberg', 'weight_1':103},
        {'source': 'Kassel', 'target': 'München', 'weight_1':502},
        {'source': 'Karlsruhe', 'target': 'Augsburg', 'weight_1':250},
        {'source': 'Nürnberg', 'target': 'Stuttgart', 'weight_1':183}
    ])

    assert bfs.solution.data.equals(expected)


def test_data():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt')
    bfs.show()

    expected = pd.DataFrame(data=[
        {'source': 'Frankfurt', 'target': 'Mannheim', 'weight_1':85},
        {'source': 'Frankfurt', 'target': 'Würzburg', 'weight_1':217},
        {'source': 'Frankfurt', 'target': 'Kassel', 'weight_1':173},
        {'source': 'Mannheim', 'target': 'Karlsruhe', 'weight_1':80},
        {'source': 'Würzburg', 'target': 'Erfurt', 'weight_1':186},
        {'source': 'Würzburg', 'target': 'Nürnberg', 'weight_1':103},
        {'source': 'Kassel', 'target': 'München', 'weight_1':502},
        {'source': 'Karlsruhe', 'target': 'Augsburg', 'weight_1':250}
    ])

    assert bfs.solution.data.equals(expected)


def test_data_end():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data)
    bfs = BFS(graph)
    bfs.run('Frankfurt', end_vertex='Erfurt', show_end=True)

    expected = pd.DataFrame(data=[
        {'source': 'Würzburg', 'target': 'Erfurt'},
        {'source': 'Frankfurt', 'target': 'Würzburg'}
    ])

    assert bfs.solution.data.equals(pd.DataFrame(expected))


def test_data_missing_source():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Random')
    bfs.show()

    assert bfs.solution.data.empty


def test_data_missing_target():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt', 'Random')
    bfs.show()

    assert bfs.solution.data.empty


def test_data_equal():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt', 'Frankfurt')
    bfs.show()

    assert bfs.solution.data.empty


def test_data_dash():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', show_end=True)


def test_data_dash_end():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', end_vertex='Erfurt', show_end=True)


def test_data_dash_equal():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', end_vertex='Frankfurt', show_end=True)


def test_data_bidirectional_dash():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', show_end=True)
