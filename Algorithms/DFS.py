from collections import deque

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer


class DFS(Algorithm):
    """
    Depth-First Search algorithm implementation. The algorithm starts at the root node and explores as far as possible
    along each branch before backtracking. The objective of this algorithm is to visit each vertex in a uniform manner.
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
            bidirectional=graph.bidirectional
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
        self.__dfs_recursion(start_vertex, end_vertex, show_by_step, show_end)

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution)

    def __dfs_recursion(self, start_vertex, end_vertex=None, show_by_step=False, show_end=False):
        self.graph.add_explored_vertex(start_vertex)
        if start_vertex == end_vertex:
            return True

        for successor in self.graph.get_successors(start_vertex):
            if not self.graph.is_explored(successor):
                self.solution.add_edge(start_vertex, successor)
                finished = self.__dfs_recursion(successor, end_vertex, show_by_step, show_end)
                if finished:
                    return True
        return False
