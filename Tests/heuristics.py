from Heuristics.Heuristic import Heuristic
from Graphs.Graph import Graph
from Heuristics.BFS import BFS


class MockedHeuristicMOA(Heuristic):

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def calculate(self, vertex):
        """
        Return a random vertex.
        :param start:
        :return:
        """
        heurs = {'s': [5,5], '1': [-1,-1], '2': [0,0], '3': [-1,-1], '4': [5,5], '5': [1,1], '6': [2,2], '7': [4,4], '8': [3,3], '9': [4,4], 'y1': [-2,-2], 'y2': [-2,-2], 'y3': [-2,-2]}
        return heurs[vertex]


class MockedHeuristicNAMOA(Heuristic):

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def calculate(self, vertex):
        """
        Return a random vertex.
        :param start:
        :return:
        """
        heurs = {'s': [3,3], 'n1': [2,2], 'n2': [2,2], 'n3': [1,1], 'n4': [1,1], 'n5': [1,1], 'n6': [0,0], 'y': [0,0]}
        return heurs[vertex]


class MockedHeuristicAutomatic(Heuristic):

    def __init__(self, graph: Graph, end_vertex):
        bfs_heur = BFS(graph)
        self.heurs = dict()
        for vertex in graph.get_all_vertices():
            self.heurs.update({vertex: bfs_heur.calculate(vertex, end_vertex)})
        super().__init__(graph)

    def calculate(self, vertex):
        """
        Return a random vertex.
        :param start:
        :return:
        """
        return self.heurs[vertex]