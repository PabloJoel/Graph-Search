import pandas as pd

from Graphs.Graph import Graph
from Visualizers.DashVisualizer import DashVisualizer
from Algorithms.Dijkstra import Dijkstra


def test_data_bidirectional():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = Dijkstra(graph)
    bfs.run(start_vertex='a')
    bfs.show()

    expected = pd.DataFrame(data=[
        {'source': 'b', 'target': 'd', 'weight_1': 5},
        {'source': 'd', 'target': 'b', 'weight_1': 5},
        {'source': 'b', 'target': 'e', 'weight_1': 6},
        {'source': 'e', 'target': 'b', 'weight_1': 6},
        {'source': 'b', 'target': 'a', 'weight_1': 2},
        {'source': 'a', 'target': 'b', 'weight_1': 2},
        {'source': 'd', 'target': 'f', 'weight_1': 2},
        {'source': 'f', 'target': 'd', 'weight_1': 2},
        {'source': 'f', 'target': 'c', 'weight_1': 3},
        {'source': 'c', 'target': 'f', 'weight_1': 3}
    ])

    assert bfs.solution.data.equals(expected)


def test_data_bidirectional_dash():
    data = pd.read_csv('dijkstra-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = Dijkstra(graph, visualizer=DashVisualizer())
    bfs.run(start_vertex='a', show_end=True)

    expected = pd.DataFrame(data=[
        {'source': 'b', 'target': 'd', 'weight_1': 5},
        {'source': 'd', 'target': 'b', 'weight_1': 5},
        {'source': 'b', 'target': 'e', 'weight_1': 6},
        {'source': 'e', 'target': 'b', 'weight_1': 6},
        {'source': 'b', 'target': 'a', 'weight_1': 2},
        {'source': 'a', 'target': 'b', 'weight_1': 2},
        {'source': 'd', 'target': 'f', 'weight_1': 2},
        {'source': 'f', 'target': 'd', 'weight_1': 2},
        {'source': 'f', 'target': 'c', 'weight_1': 3},
        {'source': 'c', 'target': 'f', 'weight_1': 3}
    ])

    assert bfs.solution.data.equals(expected)