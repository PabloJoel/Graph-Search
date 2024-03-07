import pandas as pd

from Graphs.Graph import Graph
from Algorithms.BDijkstra import Heap, BDijkstra
from Visualizers.DashVisualizer import DashVisualizer


def heap_verification(heap_object):
    heap = heap_object.heap
    for index in range(len(heap)):
        successor_index = 2 * index
        if successor_index+1 > len(heap)-1 or successor_index+2 > len(heap)-1:
            return True
        elif heap_object._check_dominance(heap[index], heap[successor_index+1]) or heap_object._check_dominance(heap[index], heap[successor_index+2]):
            return False
    return True


def check_dominance(costs1, costs2):
    if len(costs1) != len(costs2):
        raise ValueError(f"Error, both costs must have the same size, but cost1:{costs1} and cost2:{costs2} have different sizes")

    as_good = True
    is_better = False

    c1, t1 = costs1[0], costs1[1]
    c2, t2 = costs2[0], costs2[1]
    if c2 > c1 or t2 > t1:
        as_good = False  # List2 is worse than List1

    if c2 < c1 or t2 < t1:
        is_better = True  # List2 is better than Cost1

    return as_good and is_better


def test_heap():
    elements = [('a',1,1),('b',2,2),('c',0,0),('d',-1,-1),('e',-2,0),('f',0,-2),('g',1,0),('h',-2,-3)]
    heap = Heap()
    for elem in elements:
        heap.push(elem)
    assert heap_verification(heap)
    assert heap.size() == 8

    first = heap.pop()
    assert heap_verification(heap)
    assert heap.size() == 7
    assert first == ('h',-2,-3)
    assert not heap.contains_vertex('h')
    assert heap.contains_vertex('a')

    heap.decrease_key(('a',0,0))
    assert heap_verification(heap)
    assert heap.contains_vertex('a')
    assert heap.size() == 7

    heap.remove(('b',2,2))
    assert heap_verification(heap)
    assert not heap.contains_vertex('b')
    assert heap.size() == 6


def test_BDijkstra_namoa_graph():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    bdijkstra = BDijkstra(graph)
    bdijkstra.run(start_vertex='s', end_vertex='y', show_end=True)

    # cost: 4,10
    path1 = pd.DataFrame(data=(
        {'source': 'n4', 'target': 'y', 'weight_1': 1, 'weight_2': 5},
        {'source': 'n2', 'target': 'n4', 'weight_1': 1, 'weight_2': 4},
        {'source': 's', 'target': 'n2', 'weight_1': 2, 'weight_2': 1}
    ))

    # cost: 9,3
    path2 = pd.DataFrame(data=[
        {'source': 'n5', 'target': 'y', 'weight_1': 1, 'weight_2': 1},
        {'source': 'n2', 'target': 'n5', 'weight_1': 6, 'weight_2': 1},
        {'source': 's', 'target': 'n2', 'weight_1': 2, 'weight_2': 1}
    ])

    print(str(bdijkstra.metrics))

    solutions = bdijkstra.solution
    assert solutions.get_solution('y')[0].data.equals(path1)
    assert solutions.get_solution('y')[0].get_path_cost(start='s', end='y') == [4,10]

    assert solutions.get_solution('y')[1].data.equals(path2)
    assert solutions.get_solution('y')[1].get_path_cost(start='s', end='y') == [9,3]


def test_BDijkstra_moa_graph_y3():
    # Using the MOA graph
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    bdijkstra = BDijkstra(graph)
    bdijkstra.run(start_vertex='s', end_vertex='y3', show_end=True)

    # cost: 5, 11
    path1 = pd.DataFrame(data=[
        {'source': '9', 'target': 'y3', 'weight_1': 1, 'weight_2': 2},
        {'source': '6', 'target': '9', 'weight_1': 2, 'weight_2': 4},
        {'source': '3', 'target': '6', 'weight_1': 1, 'weight_2': 2},
        {'source': 's', 'target': '3', 'weight_1': 1, 'weight_2': 3}
    ])

    # cost: 6, 7
    path2 = pd.DataFrame(data=[
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2}
    ])

    # cost: 9, 5
    path3 = pd.DataFrame(data=[
        {'source': '8', 'target': 'y3', 'weight_1': 3, 'weight_2': 2},
        {'source': '5', 'target': '8', 'weight_1': 1, 'weight_2': 1},
        {'source': '2', 'target': '5', 'weight_1': 2, 'weight_2': 1},
        {'source': 's', 'target': '2', 'weight_1': 3, 'weight_2': 1}
    ])

    solutions = bdijkstra.solution
    assert solutions.get_solution('y3')[0].data.equals(path1)
    assert solutions.get_solution('y3')[1].data.equals(path2)
    assert solutions.get_solution('y3')[2].data.equals(path3)

    assert solutions.get_solution('y3')[0].get_path_cost(start='s', end='y3') == [5,11]
    assert solutions.get_solution('y3')[1].get_path_cost(start='s', end='y3') == [6,7]
    assert solutions.get_solution('y3')[2].get_path_cost(start='s', end='y3') == [9,5]


def test_BDijkstra_moa_graph_y1():
    # Using the MOA graph
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    bdijkstra = BDijkstra(graph)
    bdijkstra.run(start_vertex='s', end_vertex='y1', show_end=True)

    # cost: 4, 11
    path1 = pd.DataFrame(data=[
        {'source': '7', 'target': 'y1', 'weight_1': 1, 'weight_2': 4},
        {'source': '5', 'target': '7', 'weight_1': 1, 'weight_2': 3},
        {'source': '1', 'target': '5', 'weight_1': 1, 'weight_2': 2},
        {'source': 's', 'target': '1', 'weight_1': 1, 'weight_2': 2}
    ])

    solutions = bdijkstra.solution
    assert solutions.get_solution('y1')[0].data.equals(path1)
    assert solutions.get_solution('y1')[0].get_path_cost(start='s', end='y1') == [4,11]


def test_namoa_missing_source():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1','weight_2'])
    bdijkstra = BDijkstra(graph)
    bdijkstra.run(start_vertex='fg', end_vertex='y', show_end=True)

    assert bdijkstra.solution.get_solution('y') is None


def test_namoa_missing_target():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    bdijkstra = BDijkstra(graph)
    bdijkstra.run(start_vertex='s', end_vertex='fdgy', show_end=True)

    assert bdijkstra.solution.get_solution('fdgy') is None


def test_namoa_missing_equal():
    data = pd.read_csv('moa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    bdijkstra = BDijkstra(graph)
    bdijkstra.run(start_vertex='s', end_vertex='s', show_end=True)

    assert bdijkstra.solution.get_solution('s') is None


def test_pulse_dash():
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    bdijkstra = BDijkstra(graph, visualizer=DashVisualizer())
    bdijkstra.run(start_vertex='s', end_vertex='y', show_end=True)


def test_pulse_dash_by_step():
    return
    data = pd.read_csv('namoa-data.csv')
    graph = Graph(data, bidirectional=False, weight_cols=['weight_1', 'weight_2'])
    bdijkstra = BDijkstra(graph, visualizer=DashVisualizer())
    bdijkstra.run(start_vertex='s', end_vertex='y', show_by_step=True, show_end=True)