import pandas as pd

from Visualizers.ConsoleVisualizer import ConsoleVisualizer
from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph


def test_graph_data():
    graph = Graph(pd.read_csv('graph-data.csv'))
    algorithm = Algorithm(graph, ConsoleVisualizer())
    assert algorithm.solution.get_all_solutions() == list()