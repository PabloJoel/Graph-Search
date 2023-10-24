from Heuristics.Heuristic import Heuristic
from Graphs.Graph import Graph
from Algorithms.BFS import BFS as BFSAlgorithm


class BFS(Heuristic):

    def __init__(self, graph: Graph):
        super().__init__(graph)

    def calculate(self, start, end):
        """
        Calculate Breath First Search path between start and end, then returns the sum of costs of that path.
        :param start:
        :param end:
        :return:
        """
        if start == end:
            return 0
        else:
            bfs = BFSAlgorithm(self.graph)
            bfs.run(start, end)
            if bfs.solution.data.empty:
                return float('inf')
            else:
                return len(bfs.solution.get_path_uninformed(start, end).data)
