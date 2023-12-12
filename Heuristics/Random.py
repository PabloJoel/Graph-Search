import random

from Heuristics.Heuristic import Heuristic
from Graphs.Graph import Graph


class Random(Heuristic):

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def calculate(self, vertices):
        """
        Return a random vertex.
        :param start:
        :return:
        """
        if len(vertices) == 0:
            raise ValueError(f"The vertices input is empty: {vertices}")
        else:
            return random.sample(vertices,1)[0]
