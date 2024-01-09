import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer
from Solution.Solution import Solution


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

        super().__init__(graph, visualizer)

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
        solution = Graph(
            data=pd.DataFrame(),
            source_col=self.graph.source_col,
            target_col=self.graph.target_col,
            bidirectional=False,
            weight_cols=self.graph.weight_cols
        )

        found = self.__dfs_recursion(start_vertex, solution, end_vertex, show_by_step, show_end)

        if found and end_vertex is not None and not solution.data.empty:
            self.solution.add_solution(end_vertex, solution)

        if len(self.solution.get_all_solutions()) == 0 and len(solution.data) > 0 and end_vertex is None and not solution.data.empty:
            self.solution.add_solution('*', solution)

        if not found and end_vertex is not None:
            print(f'Warning, could not find a path to {end_vertex}')

        if show_end:
            self.visualizer.show(graph=self.graph)
            for solution in self.solution.get_all_solutions():
                self.visualizer.show(graph=solution)

    def __dfs_recursion(self, start_vertex, solution, end_vertex=None, show_by_step=False, show_end=False):
        self.graph.add_explored_vertex(start_vertex)
        if start_vertex == end_vertex:
            return True

        for successor in self.graph.get_successors(start_vertex):
            if not self.graph.is_explored(successor):
                weight = self.graph.get_weight(start_vertex, successor)
                solution.add_edge(start_vertex, successor, weight)
                finished = self.__dfs_recursion(successor, solution, end_vertex, show_by_step, show_end)
                if finished:
                    return True
        return False
