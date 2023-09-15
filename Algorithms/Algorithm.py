from abc import abstractmethod
import pandas as pd

from Graphs.Graph import Graph


class Algorithm:

    def __init__(self, graph: Graph):
        self.graph = graph
        self.solution = Graph(pd.DataFrame())

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

