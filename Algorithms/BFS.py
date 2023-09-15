from collections import deque

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph


class BFS(Algorithm):
    """
    Breath-First Search algorithm
    """

    def __init__(self, graph: Graph):
        """
        Creates the algorithm by using the input graph that contains the data, and by creating an empty Graph where the
        solution is going to be added later.
        The solution graph is created using the same parameters as the input graph, but empty.
        :param Graph graph: input graph containing the data.
        """
        solution = Graph(
            data=pd.DataFrame(),
            source_col=graph.source_col,
            target_col=graph.target_col,
            bidirectional=graph.bidirectional
        )
        super().__init__(graph, solution)

    def step(self):
        pass

    def run(self, start_vertex, end_vertex=None):
        """
        Runs the algorithm from start_vertex until there are no more vertex to explore or end_vertex has been explored.
        :param start_vertex:
        :param end_vertex:
        :return:
        """
        queue = deque()
        queue.append(start_vertex)
        self.graph.add_explored_vertex(start_vertex)

        while len(queue) > 0:
            node = queue.popleft()
            if node == end_vertex:
                return
            else:
                for successor in self.graph.get_successors(node):
                    if not self.graph.is_explored(successor):
                        self.graph.add_explored_vertex(successor)
                        queue.append(successor)
                        self.solution.add_vertex(node, successor)




