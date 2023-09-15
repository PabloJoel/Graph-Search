import pandas as pd

from Graphs.Graph import Graph
from Algorithms.BFS import BFS


def test_data():
    data = pd.read_csv('bfs-data.csv')
    graph = Graph(data, bidirectional=True)
    bfs = BFS(graph)
    bfs.run('Frankfurt')
    bfs.show()
