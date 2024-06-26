from collections import deque

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.PandasGraph import PandasGraph
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

        super().__init__(graph, visualizer)

    def run(self, start_vertex, end_vertex=None, show_by_step=False, show_end=False):
        """
        Runs the algorithm from start_vertex until there are no more vertices to explore or end_vertex has been explored.
        :param start_vertex:
        :param end_vertex:
        :return:
        """
        queue = deque()
        queue.append(start_vertex)
        explored_vertices = set()
        explored_vertices.add(start_vertex)

        solution = PandasGraph(
            data=pd.DataFrame(),
            source_col=self.graph.source_col,
            target_col=self.graph.target_col,
            bidirectional=False,
            weight_cols=self.graph.weight_cols
        )

        finished = False
        while len(queue) > 0 and not finished:
            self.metrics.add_explored_node()
            node = queue.popleft()
            successors = self.graph.get_successors(node)

            if show_by_step:
                self.visualizer.wait(graph=self.graph, current=node, open=successors, close=explored_vertices)

            if node == end_vertex:
                finished = True
                self.solution.add_solution(end_vertex, solution.get_path_uninformed(start_vertex, end_vertex))
            else:
                for successor in successors:
                    if successor not in explored_vertices:
                        explored_vertices.add(successor)
                        queue.append(successor)
                        weight = self.graph.get_weight(node, successor)
                        solution.add_edge(node, successor, weights=weight)

        self.metrics.end_execution()
        if len(self.solution.get_all_solutions()) == 0 and len(solution.data) > 0 and end_vertex is None:
            self.solution.add_solution('*', solution)

        if not finished and end_vertex is not None:
            print(f'Warning, could not find a path to {end_vertex}')

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution.get_all_solutions())



