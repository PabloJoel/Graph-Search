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


def test_namoa_inverse():
    graph = Graph(data=pd.read_csv('namoa-data.csv'), weight_cols=['weight_1', 'weight_2'])
    visualizer = DashVisualizer()

    inverse_graph = graph.get_inverse_graph()
    inverse_graph_c = inverse_graph
    inverse_graph_t = inverse_graph.copy()

    inverse_graph_c.weight_cols = ['weight_1']
    inverse_graph_t.weight_cols = ['weight_2']

    dijkstra_c = Dijkstra(inverse_graph_c)
    dijkstra_c.run(start_vertex='y')
    inverse_c_sol = dijkstra_c.solution
    c_graph = inverse_c_sol.get_solution('*')[0]
    c_graph.weight_cols = ['weight_1', 'weight_2']
    c_graph.data['weight_2'] = c_graph.data.apply(
        lambda data: graph.get_weight(data[graph.target_col], data[graph.source_col])[1], axis=1)
    visualizer.show(graph=c_graph)

    dijkstra_t = Dijkstra(inverse_graph_t)
    dijkstra_t.run(start_vertex='y')
    inverse_t_sol = dijkstra_t.solution
    t_graph = inverse_t_sol.get_solution('*')[0]
    t_graph.weight_cols = ['weight_1', 'weight_2']
    t_graph.data['weight_1'] = t_graph.data.apply(
        lambda data: graph.get_weight(data[graph.target_col], data[graph.source_col])[0], axis=1)
    visualizer.show(graph=t_graph)


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
