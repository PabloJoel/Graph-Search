import pandas as pd

from Graphs.Graph import Graph
from Algorithms.AStar import AStar
from Visualizers.DashVisualizer import DashVisualizer


def test_astar():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    a_star = AStar(graph)
    a_star.run(start_vertex='a', end_vertex='f', show_end=True)

    expected = [
        {'source': 'd', 'target': 'f', 'weight_1': 1},
        {'source': 'c', 'target': 'd', 'weight_1': 6},
        {'source': 'a', 'target': 'c', 'weight_1': 3}
    ]

    assert a_star.solution.data.equals(pd.DataFrame(expected))


def test_astar_bidirectional():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    a_star = AStar(graph)
    a_star.run(start_vertex='a', end_vertex='f', show_end=True)

    expected = [
        {'source': 'd', 'target': 'f', 'weight_1': 1},
        {'source': 'c', 'target': 'd', 'weight_1': 6},
        {'source': 'a', 'target': 'c', 'weight_1': 3}
    ]

    assert a_star.solution.data.equals(pd.DataFrame(expected))


def test_astar_dash():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    a_star = AStar(graph, visualizer=DashVisualizer())
    a_star.run(start_vertex='a', end_vertex='f', show_end=True)

    expected = [
        {'source': 'd', 'target': 'f', 'weight_1': 1},
        {'source': 'c', 'target': 'd', 'weight_1': 6},
        {'source': 'a', 'target': 'c', 'weight_1': 3}
    ]

    assert a_star.solution.data.equals(pd.DataFrame(expected))


def test_astar_bidirectional_dash():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    a_star = AStar(graph, visualizer=DashVisualizer())
    a_star.run(start_vertex='a', end_vertex='f', show_end=True)

    expected = [
        {'source': 'd', 'target': 'f', 'weight_1': 1},
        {'source': 'c', 'target': 'd', 'weight_1': 6},
        {'source': 'a', 'target': 'c', 'weight_1': 3}
    ]

    assert a_star.solution.data.equals(pd.DataFrame(expected))