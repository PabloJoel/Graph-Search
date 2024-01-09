import pandas as pd

from Graphs.Graph import Graph
from Visualizers.DashVisualizer import DashVisualizer
from Algorithms.Dijkstra import Dijkstra


def test_data_bidirectional():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1'])
    dijkstra = Dijkstra(graph)
    dijkstra.run(start_vertex='a')
    dijkstra.show()

    expected = pd.DataFrame(data=[
        {'source': 'a', 'target': 'b', 'weight_1': 2},
        {'source': 'b', 'target': 'd', 'weight_1': 5},
        {'source': 'b', 'target': 'e', 'weight_1': 6},
        {'source': 'd', 'target': 'f', 'weight_1': 2},
        {'source': 'f', 'target': 'c', 'weight_1': 3}
    ])

    assert dijkstra.solution.get_solution('*')[0].data.equals(expected)

    assert dijkstra.solution.get_solution('a')[0].get_path_cost(start='a', end='a') == [0]
    assert dijkstra.solution.get_solution('b')[0].get_path_cost(start='a', end='b') == [2]
    assert dijkstra.solution.get_solution('c')[0].get_path_cost(start='a', end='c') == [12]
    assert dijkstra.solution.get_solution('d')[0].get_path_cost(start='a', end='d') == [7]
    assert dijkstra.solution.get_solution('e')[0].get_path_cost(start='a', end='e') == [8]
    assert dijkstra.solution.get_solution('f')[0].get_path_cost(start='a', end='f') == [9]


def test_data_bidirectional_finish():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    dijkstra = Dijkstra(graph)
    dijkstra.run(start_vertex='a', end_vertex='c', show_end=True)

    expected = pd.DataFrame(data=[
        {'source': 'f', 'target': 'c', 'weight_1': 3},
        {'source': 'd', 'target': 'f', 'weight_1': 2},
        {'source': 'b', 'target': 'd', 'weight_1': 5},
        {'source': 'a', 'target': 'b', 'weight_1': 2}
    ])

    assert dijkstra.solution.get_solution('c')[0].data.equals(expected)

    assert dijkstra.solution.get_solution('c')[0].get_path_cost(start='a', end='c') == [12]


def test_data_missing_source():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    dijkstra = Dijkstra(graph)
    dijkstra.run(start_vertex='Random')
    dijkstra.show()

    assert dijkstra.solution.get_solution('Random') is None


def test_data_missing_target():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    dijkstra = Dijkstra(graph)
    dijkstra.run(start_vertex='a', end_vertex='Random', show_end=True)

    assert dijkstra.solution.get_solution('Random') is None


def test_data_equal():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    dijkstra = Dijkstra(graph)
    dijkstra.run(start_vertex='a', end_vertex='a', show_end=True)

    assert dijkstra.solution.get_solution('a') is None


def test_data_bidirectional_dash():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    dijkstra = Dijkstra(graph, visualizer=DashVisualizer())
    dijkstra.run(start_vertex='a', show_end=True)


def test_data_bidirectional_finish_dash():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    dijkstra = Dijkstra(graph, visualizer=DashVisualizer())
    dijkstra.run(start_vertex='a', end_vertex='c', show_end=True)
