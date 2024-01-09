import pandas as pd

from Graphs.Graph import Graph
from Algorithms.NAMOA import NAMOA

from Visualizers.DashVisualizer import DashVisualizer
from Tests.heuristics import MockedHeuristicMOA, MockedHeuristicNAMOA


def test_namoa():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristicNAMOA)
    namoa.run(start_vertex='s', end_vertices='y', show_end=True)

    path1 = pd.DataFrame(data=[
        {'source': 'n4', 'target': 'y', 'weight_1': 1, 'weight_2': 5},
        {'source': 'n2', 'target': 'n4', 'weight_1': 1, 'weight_2': 4},
        {'source': 's', 'target': 'n2', 'weight_1': 2, 'weight_2': 1}
    ])

    path2 = pd.DataFrame(data=[
        {'source': 'n5', 'target': 'y', 'weight_1': 1, 'weight_2': 1},
        {'source': 'n2', 'target': 'n5', 'weight_1': 6, 'weight_2': 1},
        {'source': 's', 'target': 'n2', 'weight_1': 2, 'weight_2': 1}
    ])

    solutions = namoa.solution
    assert solutions.get_solution('y')[0].data.equals(path1)
    assert solutions.get_solution('y')[1].data.equals(path2)

    assert solutions.get_solution('y')[0].get_path_cost(start='s', end='y') == [4,10]
    assert solutions.get_solution('y')[1].get_path_cost(start='s', end='y') == [9,3]


def test_namoa2():
    # Using the MOA graph
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristicMOA)
    namoa.run(start_vertex='s', end_vertices=['y1','y2','y3'], show_end=True)

    # cost: 6, 7
    path1 = pd.DataFrame(data=[
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2}
    ])

    # cost: 9, 5
    path2 = pd.DataFrame(data=[
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '2', 'target': '5', 'weight_1': 2, 'weight_2': 1},
        {'source': 's', 'target': '2', 'weight_1': 3, 'weight_2': 1}
    ])

    # cost: 4, 11
    path3 = pd.DataFrame(data=[
        {'source': '7', 'target': 'y1', 'weight_1': 1, 'weight_2': 4},
        {'source': '5', 'target': '7', 'weight_1': 1, 'weight_2': 3},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2}
    ])

    solutions = namoa.solution
    assert solutions.get_solution('y3')[0].data.equals(path1)
    assert solutions.get_solution('y3')[1].data.equals(path2)
    assert solutions.get_solution('y1')[0].data.equals(path3)

    assert solutions.get_solution('y3')[0].get_path_cost(start='s', end='y3') == [6,7]
    assert solutions.get_solution('y3')[1].get_path_cost(start='s', end='y3') == [9,5]
    assert solutions.get_solution('y1')[0].get_path_cost(start='s', end='y1') == [4,11]


def test_namoa_missing_source():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristicNAMOA)
    namoa.run(start_vertex='fg', end_vertices='y', show_end=True)

    assert namoa.solution.get_solution('y') is None


def test_namoa_missing_target():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristicNAMOA)
    namoa.run(start_vertex='s', end_vertices='fdgh', show_end=True)

    assert namoa.solution.get_solution('fdgh') is None


def test_namoa_missing_equal():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristicNAMOA)
    namoa.run(start_vertex='s', end_vertices='s', show_end=True)

    assert namoa.solution.get_solution('s') is None


def test_namoa_dash():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristicNAMOA, visualizer=DashVisualizer())
    namoa.run(start_vertex='s', end_vertices='y', show_end=True)

