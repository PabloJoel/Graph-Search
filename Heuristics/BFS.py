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
            solution = bfs.solution.get_solution(end)
            if solution is not None and len(solution) > 0 and len(solution[0].data) > 0:
                return len(solution[0].get_path_uninformed(start, end).data)
            else:
                return float('inf')

