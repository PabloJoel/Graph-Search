from collections import deque

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer


class BFS(Algorithm):
    """
    Breath-First Search algorithm implementation. This algorithm search all vertices at distance k, before moving to
    distance k+1. In the end, it creates a graph minimizing distances (it doesn't take into account weights).
    """

    def __init__(self, graph: Graph, visualizer=ConsoleVisualizer()):
        """
        Creates the algorithm by using the input graph that contains the data, and by creating an empty Graph where the
        solution is going to be added later.
        The solution graph is created using the same parameters as the input graph, but empty.
        :param Graph graph: input graph containing the data.
        :param Visualizer visualizer: visualizer implementation to visualize the graphs. By default: ConsoleVisualizer.
        """
        solution = Graph(
            data=pd.DataFrame(),
            source_col=graph.source_col,
            target_col=graph.target_col,
            bidirectional=False,
            weight_cols=graph.weight_cols
        )
        super().__init__(graph, solution, visualizer)

    def step(self):
        """
        Run one step of the algorithm.
        :return:
        """
        pass

    def run(self, start_vertex, end_vertex=None, show_by_step=False, show_end=False):
        """
        Runs the algorithm from start_vertex until there are no more vertices to explore or end_vertex has been explored.
        :param start_vertex:
        :param end_vertex:
        :return:
        """
        queue = deque()
        queue.append(start_vertex)
        self.graph.add_explored_vertex(start_vertex)

        finished = False
        while len(queue) > 0 and not finished:
            node = queue.popleft()
            if node == end_vertex:
                finished = True
            else:
                for successor in self.graph.get_successors(node):
                    if not self.graph.is_explored(successor):
                        self.graph.add_explored_vertex(successor)
                        queue.append(successor)
                        weight = self.graph.get_weight(node, successor)
                        self.solution.add_edge(node, successor, weights=weight)
        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution)



