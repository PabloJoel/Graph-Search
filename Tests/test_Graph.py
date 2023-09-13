import pandas as pd
from Graph.Graph import Graph


def test_data():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert data.equals(graph.data)


def test_predecessors_empty():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert graph.get_predecessors('s').empty


def test_predecessors():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)

    source = ['n1','n1','n1','n3','n4','n4']
    target = ['n3','n4','n6','n6','n6','t']
    dir = ['unidirectional','unidirectional','unidirectional','unidirectional','unidirectional','unidirectional']
    weight1 = [1,3,3,2,6,1]
    weight2 = [9,2,8,3,4,5]
    predecessors = pd.DataFrame(data={'source': source, 'target': target, 'direction': dir, 'weight_1': weight1, 'weight_2': weight2})

    assert graph.get_predecessors('n6').equals(predecessors)


def test_successors_empty():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)
    assert graph.get_successors('t').empty


def test_successors():
    data = pd.read_csv('graph-data.csv')
    graph = Graph(data)

    source = ['n4', 'n4', 'n5']
    target = ['n6', 't', 't']
    dir = ['unidirectional', 'unidirectional', 'unidirectional']
    weight1 = [6,1,1]
    weight2 = [4,5,1]
    successors = pd.DataFrame(data={'source': source, 'target': target, 'direction': dir, 'weight_1': weight1, 'weight_2': weight2})

    assert graph.get_successors('n2').equals(successors)
