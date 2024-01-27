import pandas as pd

from Graphs.Graph import Graph
from Algorithms.PULSE import PULSE

from Visualizers.DashVisualizer import DashVisualizer


def test_pulse():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    pulse = PULSE(graph)
    pulse.run(start_vertex='s', end_vertex='y', show_end=True)

    path1 = pd.DataFrame(data=(
        {'source': 's', 'target': 'n2', 'weight_1': 2, 'weight_2': 1},
        {'source': 'n2', 'target': 'n4', 'weight_1': 1, 'weight_2': 4},
        {'source': 'n4', 'target': 'y', 'weight_1': 1, 'weight_2': 5}
    ))

    path2 = pd.DataFrame(data=(
        {'source': 's', 'target': 'n2', 'weight_1': 2, 'weight_2': 1},
        {'source': 'n2', 'target': 'n5', 'weight_1': 6, 'weight_2': 1},
        {'source': 'n5', 'target': 'y', 'weight_1': 1, 'weight_2': 1}
    ))

    solutions = pulse.solution
    assert solutions.get_solution('y')[0].data.equals(path1)
    assert solutions.get_solution('y')[1].data.equals(path2)

    assert solutions.get_solution('y')[0].get_path_cost(start='s', end='y') == [4,10]
    assert solutions.get_solution('y')[1].get_path_cost(start='s', end='y') == [9,3]


def test_pulse_moa_graph_y1():
    # Using the MOA graph
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    pulse = PULSE(graph)
    pulse.run(start_vertex='s', end_vertex='y1', show_end=True)

    # cost: 4, 11
    path1 = pd.DataFrame(data=[
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': '5', 'target': '7', 'weight_1': 1, 'weight_2': 3},
        {'source': '7', 'target': 'y1', 'weight_1': 1, 'weight_2': 4}
    ])

    solutions = pulse.solution
    assert solutions.get_solution('y1')[0].data.equals(path1)
    assert solutions.get_solution('y1')[0].get_path_cost(start='s', end='y1') == [4,11]


def test_pulse_moa_graph_y3():
    # Using the MOA graph
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    pulse = PULSE(graph)
    pulse.run(start_vertex='s', end_vertex='y3', show_end=True)

    # cost: 6, 7
    path1 = pd.DataFrame(data=[
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
    ])

    # cost: 9, 5
    path2 = pd.DataFrame(data=[
        {'source': 's', 'target': '2', 'weight_1': 3, 'weight_2': 1},
        {'source': '2', 'target': '5', 'weight_1': 2, 'weight_2': 1},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
    ])

    # cost: 5, 11
    path3 = pd.DataFrame(data=[
        {'source': 's', 'target': '3', 'weight_1': 1, 'weight_2': 3},
        {'source': '3', 'target': '6', 'weight_1': 1, 'weight_2': 2},
        {'source': '6', 'target': '9', 'weight_1': 2, 'weight_2': 4},
        {'source': '9', 'target': 'y3', 'weight_1': 1, 'weight_2': 2}
    ])

    solutions = pulse.solution
    assert solutions.get_solution('y3')[0].data.equals(path1)
    assert solutions.get_solution('y3')[1].data.equals(path2)
    assert solutions.get_solution('y3')[2].data.equals(path3)

    assert solutions.get_solution('y3')[0].get_path_cost(start='s', end='y3') == [6,7]
    assert solutions.get_solution('y3')[1].get_path_cost(start='s', end='y3') == [9,5]
    assert solutions.get_solution('y3')[2].get_path_cost(start='s', end='y3') == [5,11]


def test_namoa_missing_source():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    pulse = PULSE(graph)
    pulse.run(start_vertex='fg', end_vertex='y', show_end=True)

    assert pulse.solution.get_solution('y') is None


def test_namoa_missing_target():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    pulse = PULSE(graph)
    pulse.run(start_vertex='s', end_vertex='fdgy', show_end=True)

    assert pulse.solution.get_solution('fdgy') is None


def test_namoa_missing_equal():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    pulse = PULSE(graph)
    pulse.run(start_vertex='s', end_vertex='s', show_end=True)

    assert pulse.solution.get_solution('s') is None


def test_pulse_dash():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    pulse = PULSE(graph, visualizer=DashVisualizer())
    pulse.run(start_vertex='s', end_vertex='y', show_end=True)


def test_dominated_empty1():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated((2, 4), ()) is False


def test_dominated_empty2():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated((), (1,3)) is True


def test_dominated_empty3():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated((), ()) is False


def test_dominated1():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated([(2,4),(3,3)], (5,2)) is False
    assert pulse.is_dominated([(2,4),(3,3)], (2,5)) is False
    assert pulse.is_dominated((5,2), (2,5)) is False
    assert pulse.is_dominated((5,2), [(2,4),(3,3)]) is False
    assert pulse.is_dominated((2,5), [(2,4),(3,3)]) is True
    assert pulse.is_dominated((2,5), (5,2)) is False


def test_dominated2():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated((5,2), (8,10)) is False
    assert pulse.is_dominated((5,2), (3,5)) is False
    assert pulse.is_dominated((2,5), (8,10)) is False
    assert pulse.is_dominated((2,5), (3,5)) is False
    assert pulse.is_dominated((8,10), (3,5)) is True
    assert pulse.is_dominated((8,10), (5,2)) is True
    assert pulse.is_dominated((8,10), (2,5)) is True
    assert pulse.is_dominated((3,5), (8,10)) is False
    assert pulse.is_dominated((3,5), (5,2)) is False
    assert pulse.is_dominated((3,5), (2,5)) is True


def test_dominated3():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated([(7,7),(4,9)], (5,2)) is False
    assert pulse.is_dominated([(7,7),(4,9)], (8,10)) is False
    assert pulse.is_dominated([(7,7),(4,9)], (3,5)) is True
    assert pulse.is_dominated((8,10), [(7,7),(4,9)]) is True
    assert pulse.is_dominated((8,10), (3,5)) is True
    assert pulse.is_dominated((8,10), (5,2)) is True


def test_dominated4():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated([(4,9),(7,6),(10,4)], [(3,5),(6,3)]) is False
    assert pulse.is_dominated([(4,9),(7,6),(10,4)], (8,10)) is False
    assert pulse.is_dominated([(3,5),(6,3)], (8,10)) is False
    assert pulse.is_dominated([(3,5),(6,3)], [(4,9),(7,6),(10,4)]) is False


def test_dominated_infinity():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    pulse = PULSE(graph)

    assert pulse.is_dominated((1,2), float('inf')) is False
    assert pulse.is_dominated(float('inf'), (1,2)) is True
    assert pulse.is_dominated(float('inf'), float('inf')) is False
    assert pulse.is_dominated([(4,9),(7,6),(10,4)], float('inf')) is False
    assert pulse.is_dominated(float('inf'), [(4,9),(7,6),(10,4)]) is True
