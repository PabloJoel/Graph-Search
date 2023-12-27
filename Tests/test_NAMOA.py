import pandas as pd

from Graphs.Graph import Graph
from Algorithms.NAMOA import NAMOA
from Heuristics.Heuristic import Heuristic
from Visualizers.DashVisualizer import DashVisualizer

class MockedHeuristic(Heuristic):

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def calculate(self, vertex):
        """
        Return a random vertex.
        :param start:
        :return:
        """
        heurs = {'s': [3,3], 'n1': [2,2], 'n2': [2,2], 'n3': [1,1], 'n4': [1,1], 'n5': [1,1], 'n6': [0,0], 'y': [0,0]}
        return heurs[vertex]


def test_namoa():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristic)
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
    assert solutions[0].data.equals(path1)
    assert solutions[1].data.equals(path2)


def test_namoa_missing_source():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristic)
    namoa.run(start_vertex='fg', end_vertices='y', show_end=True)

    assert namoa.solution[0].data.empty


def test_namoa_missing_target():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristic)
    namoa.run(start_vertex='s', end_vertices='fdgh', show_end=True)

    assert namoa.solution[0].data.empty


def test_namoa_missing_equal():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristic)
    namoa.run(start_vertex='s', end_vertices='s', show_end=True)

    assert namoa.solution[0].data.empty


def test_namoa_dash():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    namoa = NAMOA(graph, heuristic=MockedHeuristic, visualizer=DashVisualizer())
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
    assert solutions[0].data.equals(path1)
    assert solutions[1].data.equals(path2)
