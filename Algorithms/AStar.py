from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer
from Heuristics.BFS import BFS

class AStar(Algorithm):
    """
    A* algorithm
    """

    def __init__(self, graph: Graph, visualizer=ConsoleVisualizer(), heuristic=None):
        """
        Creates the algorithm by using the input graph that contains the data, and by creating an empty Graph where the
        solution is going to be added later.
        The solution graph is created using the same parameters as the input graph, but empty.
        :param Graph graph: input graph containing the data.
        :param Visualizer visualizer: visualizer implementation to visualize the graphs. By default: ConsoleVisualizer.
        :param heuristic: heuristic function to be used. By default: BFS Heuristic.
        """

        super().__init__(graph, visualizer)
        if heuristic is None:
            self.heuristic = BFS(graph)
        else:
            self.heuristic = heuristic

    def run(self, start_vertex, end_vertex=None, show_by_step=False, show_end=False):
        """
        Runs the algorithm from start_vertex until there are no more vertices to explore or end_vertex has been explored.
        :param start_vertex:
        :param end_vertex:
        :return:
        """
        all_vertices = self.graph.get_all_vertices()
        finished = False

        if start_vertex in all_vertices and end_vertex in all_vertices and start_vertex != end_vertex:
            open = {start_vertex}
            closed = set()
            prev = {}

            h = {start_vertex: self.heuristic.calculate(start_vertex, end_vertex)}
            g = {vertex: float("inf") if vertex != start_vertex else 0 for vertex in all_vertices}
            f = {vertex: float("inf") if vertex != start_vertex else h[start_vertex] for vertex in all_vertices}

            while len(open) > 0:
                self.metrics.add_explored_node()
                open_f = {node:value for node,value in f.items() if node in open}
                current = min(open_f, key=open_f.get)

                if show_by_step:
                    self.visualizer.wait(graph=self.graph, current=current, open=open, close=closed)

                if current == end_vertex:
                    self.solution.add_solution(end_vertex, self.graph.get_path_informed(start_vertex, end_vertex, prev))
                    finished = True
                    break

                open.remove(current)
                closed.add(current)
                for successor in self.graph.get_successors(current):
                    cost = self.graph.get_weight(source=current, target=successor)[0]
                    g_cost = g[current] + cost
                    if g_cost < g[successor]:
                        prev[successor] = current
                        g[successor] = g_cost
                        if successor not in h:
                            h[successor] = self.heuristic.calculate(successor, end_vertex)
                        f[successor] = g_cost + h[successor]
                        if successor not in open:
                            open.add(successor)

        self.metrics.end_execution()
        if not finished and end_vertex is not None:
            print(f'Warning, could not find a path from {start_vertex} to {end_vertex}')

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution.get_all_solutions())



