from collections import deque

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph


class BFS(Algorithm):
    """
    Breath-First Search algorithm
    """

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def step(self):
        pass

    def run(self, start_node, end_node=None):
        queue = deque()
        queue.append(start_node)
        self.graph.add_explored_node(start_node)

        while len(queue) > 0:
            node = queue.popleft()
            if start_node == end_node:
                return
            else:
                for successor in self.graph.get_successors(node):
                    if not self.graph.is_explored(successor):
                        self.graph.add_explored_node(successor)
                        queue.append(successor)
                        self.solution.add_node(node, successor)




