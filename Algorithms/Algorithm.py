from abc import abstractmethod

from Graphs.Graph import Graph


class Algorithm:

    def __init__(self, graph: Graph, solution: Graph):
        self.graph = graph
        self.solution = solution

    def show(self):
        print('Showing graph')
        self.graph.show()
        print('Showing solution')
        self.solution.show()

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def run(self):
        pass

