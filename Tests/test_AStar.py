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

    print(str(a_star.metrics))

    assert a_star.solution.get_solution('f')[0].data.equals(pd.DataFrame(expected))

    assert a_star.solution.get_solution('f')[0].get_path_cost(start='a', end='f') == [10]


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

    assert a_star.solution.get_solution('f')[0].data.equals(pd.DataFrame(expected))

    assert a_star.solution.get_solution('f')[0].get_path_cost(start='a', end='f') == [10]


def test_astar_missing_source():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    a_star = AStar(graph)
    a_star.run(start_vertex='Random', end_vertex='f', show_end=True)

    assert a_star.solution.get_solution('Random') is None


def test_astar_missing_target():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    a_star = AStar(graph)
    a_star.run(start_vertex='a', end_vertex='Random', show_end=True)

    assert a_star.solution.get_solution('Random') is None


def test_astar_equal():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    a_star = AStar(graph)
    a_star.run(start_vertex='a', end_vertex='a', show_end=True)

    assert a_star.solution.get_solution('Random') is None


def test_astar_dash():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    a_star = AStar(graph, visualizer=DashVisualizer())
    a_star.run(start_vertex='a', end_vertex='f', show_end=True)


def test_astar_bidirectional_dash():
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    a_star = AStar(graph, visualizer=DashVisualizer())
    a_star.run(start_vertex='a', end_vertex='f', show_end=True)


def test_astar_dash_by_step():
    return
    data = pd.read_csv('astar-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    a_star = AStar(graph, visualizer=DashVisualizer())
    a_star.run(start_vertex='a', end_vertex='f', show_by_step=True, show_end=True)