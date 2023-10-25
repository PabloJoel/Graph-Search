from collections import deque

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer


class Dijkstra(Algorithm):
    """
    Dijkstra algorithm
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
            weight_cols=graph.weight_cols,
            bidirectional=False
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
        all_vertices = self.graph.get_all_vertices()
        finished = False

        if start_vertex in all_vertices and start_vertex != end_vertex:
            # Initialize distances
            dist = {vertex: float("inf") if vertex != 's' else 0 for vertex in all_vertices}
            prev = {vertex: None for vertex in all_vertices}
            unexplored_vertices = all_vertices
            current_vertex = start_vertex

            while len(unexplored_vertices) > 0:
                self.graph.add_explored_vertex(current_vertex)

                if current_vertex == end_vertex:
                    self.solution = self.graph.get_path_informed(start_vertex, end_vertex, prev)
                    finished = True
                    break

                for successor in self.graph.get_successors(current_vertex):
                    # Calculate distance
                    current_dist = self.graph.get_weight(source=current_vertex, target=successor)[0]                        # Distance between current and successor
                    start_dist = 0 if dist[current_vertex] == float("inf") else dist[current_vertex]                        # Distance between current and start vertex
                    distance = current_dist + start_dist

                    # Update min distances dictionary and solution graph
                    if distance < dist[successor]:
                        predecessor = self.solution.get_predecessors(successor)
                        if len(predecessor) > 0:
                            self.solution.remove_edge(predecessor[0], successor)                                        # Remove old edge
                        self.solution.add_edge(current_vertex, successor, [current_dist])    # Add new edge
                        prev[successor] = current_vertex
                        dist[successor] = distance                                                                      # Update min distance

                # Get the unexplored vertex with the min distance
                unexplored_vertices = self.graph.get_unexplored_vertices()
                min_dist = float("inf")
                min_vertex = None
                for unexplored_vertex in unexplored_vertices:
                    unexplored_dist = dist[unexplored_vertex]
                    if unexplored_dist < min_dist:
                        min_dist = unexplored_dist
                        min_vertex = unexplored_vertex
                current_vertex = min_vertex

        if not finished and end_vertex is not None:
            print(f'Warning, could not find a path to {end_vertex}')
            self.solution.data = pd.DataFrame()

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution)



