import pandas as pd

from Graphs.Graph import Graph
from Algorithms.MOA import MOA
from Visualizers.DashVisualizer import DashVisualizer
from Tests.heuristics import MockedHeuristicMOA, MockedHeuristicNAMOA


def test_moa():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph, heuristic=MockedHeuristicMOA(graph))
    moa.run(start_vertex='s', end_vertices=['y1','y2','y3'], show_end=True)

    path1 = pd.DataFrame(data=[
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2}
    ])

    path2 = pd.DataFrame(data=[
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '2', 'target': '5', 'weight_1': 2, 'weight_2': 1},
        {'source': 's', 'target': '2', 'weight_1': 3, 'weight_2': 1}
    ])

    path3 = pd.DataFrame(data=[
        {'source': '7', 'target': 'y1', 'weight_1': 1, 'weight_2': 4},
        {'source': '5', 'target': '7', 'weight_1': 1, 'weight_2': 3},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2}
    ])

    print(str(moa.metrics))

    solutions = moa.solution
    assert solutions.get_solution_cost('s', 'y3') == [[6,7], [9,5]]
    assert solutions.get_solution_cost('s', 'y1') == [[4,11]]
    assert solutions.get_min_solution_cost('s') == [4,11]

    assert solutions.get_solution('y3')[0].data.equals(path1)
    assert solutions.get_solution('y3')[1].data.equals(path2)
    assert solutions.get_solution('y1')[0].data.equals(path3)


def test_moa2():
    # using the NAMOA graph
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph, heuristic=MockedHeuristicNAMOA(graph))
    moa.run(start_vertex='s', end_vertices=['y'], show_end=True)

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

    solutions = moa.solution
    assert solutions.get_solution('y')[0].data.equals(path1)
    assert solutions.get_solution('y')[1].data.equals(path2)

    assert solutions.get_solution_cost('s', 'y') == [[4,10],[9,3]]
    assert solutions.get_min_solution_cost('s') == [4,10]


def test_moa_missing_source():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph, heuristic=MockedHeuristicMOA(graph))
    moa.run(start_vertex='df', end_vertices=['y1','y2','y3'], show_end=True)

    assert moa.solution.get_solution('y1') is None
    assert moa.solution.get_solution('y2') is None
    assert moa.solution.get_solution('y3') is None


def test_moa_missing_target():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph, heuristic=MockedHeuristicMOA(graph))
    moa.run(start_vertex='s', end_vertices=['x','y'], show_end=True)

    assert moa.solution.get_solution('x') is None
    assert moa.solution.get_solution('y') is None


def test_moa_missing_equal():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph, heuristic=MockedHeuristicMOA(graph))
    moa.run(start_vertex='s', end_vertices=['s'], show_end=True)

    assert moa.solution.get_solution('s') is None


def test_moa_dash():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph, heuristic=MockedHeuristicMOA(graph), visualizer=DashVisualizer())
    moa.run(start_vertex='s', end_vertices=['y1','y2','y3'], show_end=True)


def test_moa_dash_by_step():
    return
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph, heuristic=MockedHeuristicMOA(graph), visualizer=DashVisualizer())
    moa.run(start_vertex='s', end_vertices=['y1','y2','y3'], show_by_step=True, show_end=True)


def test_dominated_empty1():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([2, 4], []) is False


def test_dominated_empty2():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([], [1,3]) is True


def test_dominated_empty3():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([], []) is False


def test_dominated1():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([[2,4],[3,3]], [5,2]) is False
    assert moa.is_dominated([[2,4],[3,3]], [2,5]) is False
    assert moa.is_dominated([5,2], [2,5]) is False
    assert moa.is_dominated([5,2], [[2,4],[3,3]]) is False
    assert moa.is_dominated([2,5], [[2,4],[3,3]]) is True
    assert moa.is_dominated([2,5], [5,2]) is False


def test_dominated2():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([5,2], [8,10]) is False
    assert moa.is_dominated([5,2], [3,5]) is False
    assert moa.is_dominated([2,5], [8,10]) is False
    assert moa.is_dominated([2,5], [3,5]) is False
    assert moa.is_dominated([8,10], [3,5]) is True
    assert moa.is_dominated([8,10], [5,2]) is True
    assert moa.is_dominated([8,10], [2,5]) is True
    assert moa.is_dominated([3,5], [8,10]) is False
    assert moa.is_dominated([3,5], [5,2]) is False
    assert moa.is_dominated([3,5], [2,5]) is True


def test_dominated3():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([[7,7],[4,9]], [5,2]) is False
    assert moa.is_dominated([[7,7],[4,9]], [8,10]) is False
    assert moa.is_dominated([[7,7],[4,9]], [3,5]) is True
    assert moa.is_dominated([8,10], [[7,7],[4,9]]) is True
    assert moa.is_dominated([8,10], [3,5]) is True
    assert moa.is_dominated([8,10], [5,2]) is True


def test_dominated4():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([[4,9],[7,6],[10,4]], [[3,5],[6,3]]) is False
    assert moa.is_dominated([[4,9],[7,6],[10,4]], [8,10]) is False
    assert moa.is_dominated([[3,5],[6,3]], [8,10]) is False
    assert moa.is_dominated([[3,5],[6,3]], [[4,9],[7,6],[10,4]]) is False


def test_dominated_infinity():
    data = pd.DataFrame()
    graph = Graph(data, bidirectional=False)
    moa = MOA(graph)

    assert moa.is_dominated([1,2], float('inf')) is False
    assert moa.is_dominated(float('inf'), [1,2]) is True
    assert moa.is_dominated(float('inf'), float('inf')) is False
    assert moa.is_dominated([[4,9],[7,6],[10,4]], float('inf')) is False
    assert moa.is_dominated(float('inf'), [[4,9],[7,6],[10,4]]) is True
    assert moa.is_dominated(float('inf'), float('inf')) is False


def test_nd_successors():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    moa = MOA(graph)
    assert moa._get_nd_successors('s') == [[1,2],[3,1]]



