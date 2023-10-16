from abc import abstractmethod

from Graphs.Graph import Graph


class Heuristic:

    def __init__(self, graph: Graph):
        self.graph = graph

    @abstractmethod
    def calculate(self, start, end):
        pass
