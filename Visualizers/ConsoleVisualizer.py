from Graphs.Graph import Graph
from Visualizers.Visualizer import Visualizer


class ConsoleVisualizer(Visualizer):
    """
    ConsoleVisualizer is a type of Visualizer that prints the graph data on the console.
    """
    def __init__(self):
        super().__init__()

    def show(self, graph):
        if isinstance(graph, list):
            for elem in graph:
                print(elem.data)
        elif isinstance(graph, Graph) or issubclass(type(graph), Graph):
            print(graph.data)
        else:
            raise TypeError(f"ConsoleVisualizer can only show Graph or list of Graph, not {type(graph)}")
