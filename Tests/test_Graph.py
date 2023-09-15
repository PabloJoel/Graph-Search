import pandas as pd
from Graphs.Graph import Graph


def test_data():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert data.equals(graph.data)


def test_predecessors_empty():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert graph.get_predecessors('s') == list()


def test_predecessors():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert graph.get_predecessors('n6') == ['n1','n3','n4']


def test_successors_empty():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert graph.get_successors('t') == list()


def test_successors():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert graph.get_successors('n2') == ['n4','n5','t']


def test_add_node():
    graph = Graph(pd.DataFrame())
    graph.add_node('s', 't', weights=[1,2])
    expected = pd.DataFrame(data={'source': ['s'], 'target': ['t'], 'direction': ['unidirectional'], 'weight_1': [1], 'weight_2': [2]})
    assert graph.data.equals(expected)


def test_get_weight():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert graph.get_weight('n1','n3') == {'weight_1': 1, 'weight_2': 9}
