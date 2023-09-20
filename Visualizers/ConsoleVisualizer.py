from Graphs.Graph import Graph
from Visualizers.Visualizer import Visualizer


class ConsoleVisualizer(Visualizer):
    """
    ConsoleVisualizer is a type of Visualizer that prints the graph data on the console.
    """
    def __init__(self):
        super().__init__()

    def show(self, graph: Graph):
        print(graph.data)
