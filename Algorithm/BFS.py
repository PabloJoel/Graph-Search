from Algorithm import Algorithm
from Graph.Graph import Graph


class BFS(Algorithm):
    """
    Breath-First Search algorithm
    """

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def get_graph(self):
        return self.graph

    def show(self):
        self.graph.show()

    def step(self):
        pass

    def run(self):
        pass



