from abc import abstractmethod

from Graphs.Graph import Graph
from Visualizers.Visualizer import Visualizer
from Solution.Solution import Solution
from Metrics.Metrics import Metrics


class Algorithm:
    """
    Algorithm is the interface to use to implement Algorithms. It defines the needed methods that any algorithm should
    contain.
    """
    def __init__(self, graph: Graph, visualizer: Visualizer):
        """
        :param Graph graph: input graph containing the data for the algorithm.
        :param Graph solution: output graph that will contain the result of the algorithm.
        :param Visualizer visualizer: specific Visualizer implementation to visualize the class.
        """
        self.graph = graph.copy()
        self.solution = Solution()
        self.visualizer = visualizer
        self.metrics = Metrics()

    @abstractmethod
    def run(self):
        """
        Run the algorithm, from start to end.
        :return:
        """
        pass

