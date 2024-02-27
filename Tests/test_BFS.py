import pandas as pd

from Graphs.Graph import Graph
from Algorithms.BFS import BFS
from Visualizers.DashVisualizer import DashVisualizer


def test_data_bidirectional():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True)
    bfs = BFS(graph)
    bfs.run('Frankfurt')
    bfs.show()

    expected = pd.DataFrame(data=[
        {'source': 'Frankfurt', 'target': 'Mannheim'},
        {'source': 'Frankfurt', 'target': 'Würzburg'},
        {'source': 'Frankfurt', 'target': 'Kassel'},
        {'source': 'Mannheim', 'target': 'Karlsruhe'},
        {'source': 'Würzburg', 'target': 'Erfurt'},
        {'source': 'Würzburg', 'target': 'Nürnberg'},
        {'source': 'Kassel', 'target': 'München'},
        {'source': 'Karlsruhe', 'target': 'Augsburg'},
        {'source': 'Nürnberg', 'target': 'Stuttgart'}
    ])

    assert bfs.solution.get_solution('Mannheim')[0].get_path_cost('Frankfurt', 'Mannheim') == []
    assert bfs.solution.get_solution('Würzburg')[0].get_path_cost('Frankfurt', 'Würzburg') == []
    assert bfs.solution.get_solution('Kassel')[0].get_path_cost('Frankfurt', 'Kassel') == []
    assert bfs.solution.get_solution('Karlsruhe')[0].get_path_cost('Frankfurt', 'Karlsruhe') == []
    assert bfs.solution.get_solution('Erfurt')[0].get_path_cost('Frankfurt', 'Erfurt') == []
    assert bfs.solution.get_solution('Nürnberg')[0].get_path_cost('Frankfurt', 'Nürnberg') == []
    assert bfs.solution.get_solution('München')[0].get_path_cost('Frankfurt', 'München') == []
    assert bfs.solution.get_solution('Augsburg')[0].get_path_cost('Frankfurt', 'Augsburg') == []

    assert bfs.solution.get_solution('*')[0].data.equals(expected)


def test_data():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt')
    bfs.show()

    expected = pd.DataFrame(data=[
        {'source': 'Frankfurt', 'target': 'Mannheim', 'weight_1': 85},
        {'source': 'Frankfurt', 'target': 'Würzburg', 'weight_1': 217},
        {'source': 'Frankfurt', 'target': 'Kassel', 'weight_1': 173},
        {'source': 'Mannheim', 'target': 'Karlsruhe', 'weight_1': 80},
        {'source': 'Würzburg', 'target': 'Erfurt', 'weight_1': 186},
        {'source': 'Würzburg', 'target': 'Nürnberg', 'weight_1': 103},
        {'source': 'Kassel', 'target': 'München', 'weight_1': 502},
        {'source': 'Karlsruhe', 'target': 'Augsburg', 'weight_1': 250}
    ])

    assert bfs.solution.get_solution('Mannheim')[0].get_path_cost('Frankfurt', 'Mannheim') == [85]
    assert bfs.solution.get_solution('Würzburg')[0].get_path_cost('Frankfurt', 'Würzburg') == [217]
    assert bfs.solution.get_solution('Kassel')[0].get_path_cost('Frankfurt', 'Kassel') == [173]
    assert bfs.solution.get_solution('Karlsruhe')[0].get_path_cost('Frankfurt', 'Karlsruhe') == [165]
    assert bfs.solution.get_solution('Erfurt')[0].get_path_cost('Frankfurt', 'Erfurt') == [403]
    assert bfs.solution.get_solution('Nürnberg')[0].get_path_cost('Frankfurt', 'Nürnberg') == [320]
    assert bfs.solution.get_solution('München')[0].get_path_cost('Frankfurt', 'München') == [675]
    assert bfs.solution.get_solution('Augsburg')[0].get_path_cost('Frankfurt', 'Augsburg') == [415]

    assert bfs.solution.get_solution('*')[0].data.equals(expected)


def test_data_end():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, )
    bfs = BFS(graph)
    bfs.run('Frankfurt', end_vertex='Erfurt', show_end=True)

    expected = pd.DataFrame(data=[
        {'source': 'Würzburg', 'target': 'Erfurt'},
        {'source': 'Frankfurt', 'target': 'Würzburg'}
    ])

    assert bfs.solution.get_solution('Erfurt')[0].get_path_cost('Frankfurt','Erfurt') == []

    assert bfs.solution.get_solution('Erfurt')[0].data.equals(expected)


def test_data_end2():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt', end_vertex='Erfurt', show_end=True)

    expected = pd.DataFrame(data=[
        {'source': 'Würzburg', 'target': 'Erfurt', 'weight_1': 186},
        {'source': 'Frankfurt', 'target': 'Würzburg',  'weight_1': 217}
    ])

    assert bfs.solution.get_solution('Erfurt')[0].get_path_cost('Frankfurt', 'Erfurt') == [403]

    assert bfs.solution.get_solution('Erfurt')[0].data.equals(expected)


def test_data_missing_source():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Random')
    bfs.show()

    assert bfs.solution.get_solution('Random') is None


def test_data_missing_target():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt', 'Random')
    bfs.show()

    assert bfs.solution.get_solution('Random') is None


def test_data_equal():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph)
    bfs.run('Frankfurt', 'Frankfurt')
    bfs.show()

    assert bfs.solution.get_solution('Random') is None


def test_data_dash():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', show_end=True)


def test_data_dash_end():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', end_vertex='Erfurt', show_end=True)


def test_data_dash_equal():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', end_vertex='Frankfurt', show_end=True)


def test_data_bidirectional_dash():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', show_end=True)


def test_data_dash_by_step():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, weight_cols=['weight_1'])
    bfs = BFS(graph, visualizer=DashVisualizer())
    bfs.run('Frankfurt', show_by_step=True, show_end=True)
