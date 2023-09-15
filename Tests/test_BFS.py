import pandas as pd

from Graphs.Graph import Graph
from Algorithms.BFS import BFS


def test_data_bidirectional():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True)
    bfs = BFS(graph)
    bfs.run('Frankfurt')
    bfs.show()

    expected = pd.DataFrame(data=[
        {'source': 'Frankfurt', 'target': 'Mannheim'},
        {'source': 'Mannheim', 'target': 'Frankfurt'},
        {'source': 'Frankfurt', 'target': 'Würzburg'},
        {'source': 'Würzburg', 'target': 'Frankfurt'},
        {'source': 'Frankfurt', 'target': 'Kassel'},
        {'source': 'Kassel', 'target': 'Frankfurt'},
        {'source': 'Mannheim', 'target': 'Karlsruhe'},
        {'source': 'Karlsruhe', 'target': 'Mannheim'},
        {'source': 'Würzburg', 'target': 'Erfurt'},
        {'source': 'Erfurt', 'target': 'Würzburg'},
        {'source': 'Würzburg', 'target': 'Nürnberg'},
        {'source': 'Nürnberg', 'target': 'Würzburg'},
        {'source': 'Kassel', 'target': 'München'},
        {'source': 'München', 'target': 'Kassel'},
        {'source': 'Karlsruhe', 'target': 'Augsburg'},
        {'source': 'Augsburg', 'target': 'Karlsruhe'},
        {'source': 'Nürnberg', 'target': 'Stuttgart'},
        {'source': 'Stuttgart', 'target': 'Nürnberg'},
    ])

    assert bfs.solution.data.equals(expected)


def test_data():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data)
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
        {'source': 'Karlsruhe', 'target': 'Augsburg'}    ])

    assert bfs.solution.data.equals(expected)
