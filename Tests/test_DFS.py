import pandas as pd

from Graphs.Graph import Graph
from Algorithms.DFS import DFS
from Visualizers.DashVisualizer import DashVisualizer


def test_data_bidirectional():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data, bidirectional=True)
    dfs = DFS(graph)
    dfs.run(1, end_vertex=3, show_end=True)

    expected = pd.DataFrame([
        {'source': 1, 'target': 2},
        {'source': 2, 'target': 3},
    ])

    assert dfs.solution.get_solution(3)[0].get_path_cost(1, 3) == []
    assert dfs.solution.get_solution(3)[0].data.equals(expected)


def test_data():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    dfs = DFS(graph)
    dfs.run(1, show_end=True)

    expected = pd.DataFrame([
        {'source': 1, 'target': 2},
        {'source': 2, 'target': 3},
        {'source': 3, 'target': 4},
        {'source': 3, 'target': 5},
        {'source': 2, 'target': 6},
        {'source': 1, 'target': 7},
        {'source': 1, 'target': 8},
        {'source': 8, 'target': 9},
        {'source': 9, 'target': 10},
        {'source': 9, 'target': 11},
        {'source': 8, 'target': 12}
    ])

    assert dfs.solution.get_solution(3)[0].get_path_cost(1, 3) == []
    assert dfs.solution.get_solution('*')[0].data.equals(expected)


def test_data_missing_source():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    dfs = DFS(graph)
    dfs.run('a', show_end=True)

    assert dfs.solution.get_solution(1) is None


def test_data_missing_target():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    dfs = DFS(graph)
    dfs.run(1, 'a', show_end=True)

    assert dfs.solution.get_solution(1) is None


def test_data_equal():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    dfs = DFS(graph)
    dfs.run(1, 1, show_end=True)

    assert dfs.solution.get_solution(1) is None


def test_data_bidirectional_dash():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data, bidirectional=True)
    dfs = DFS(graph, visualizer=DashVisualizer())
    dfs.run(1, end_vertex=3, show_end=True)


def test_data_dash():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    dfs = DFS(graph, visualizer=DashVisualizer())
    dfs.run(1,show_end=True)


def test_data_dash_by_step():
    data = pd.read_csv('dfs-data.csv')
    graph = Graph(data)
    dfs = DFS(graph, visualizer=DashVisualizer())
    dfs.run(1, show_by_step=True, show_end=True)

