from abc import abstractmethod

from Graphs.Graph import Graph


class Visualizer:
    """
    Visualizer interface defines the base methods needed for a Visualizer class. A visualizer is a class that allows
    the visualization of a Graph object.
    """
    def __init__(self):
        pass

    @abstractmethod
    def show(self, graph: Graph):
        pass
