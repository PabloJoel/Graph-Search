import abc

from Graph.Graph import Graph


class Algorithm(abc.ABC):

    @abc.abstractmethod
    def __init__(self, graph: Graph):
        self.graph = graph

    @abc.abstractmethod
    def get_graph(self):
        return self.graph

    @abc.abstractmethod
    def show(self):
        self.graph.show()

    @abc.abstractmethod
    def step(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

