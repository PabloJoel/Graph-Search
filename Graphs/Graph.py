from abc import abstractmethod


class Graph:
    """
    Graph is the interface to use to implement graph objects. It defines the needed methods that any Graph should
    contain.
    """

    def __init__(self):
        """
        This method loads the data that represents the Graph.
        """
        pass

    @abstractmethod
    def add_edge(self, source, target, weights=list()):
        """
        Add an edge from source to target to the graph. Optionally, a dict of weights can be added to the edge.
        :param str source: source vertex.
        :param str target:  target vertex.
        :param list weights: dict where keys are weight column names and values are the actual weights.
        :return:
        """
        pass

    @abstractmethod
    def remove_edge(self, source, target):
        """
        Remove the edge between source and target vertices, if it exists.
        :param str source: source vertex.
        :param str target:  target vertex.
        :return:
        """
        pass

    @abstractmethod
    def get_weight(self, source, target):
        """
        Returns the weights of the edge between source vertex and target vertex. If there is no connection, returns an
        empty dictionary.
        :param str source: source vertex of the edge.
        :param str target: target vertex of the edge.
        :return:
        """
        pass

    @abstractmethod
    def get_predecessors(self, vertex):
        """
        Get the predecessors of a given vertex.
        :param str vertex:
        :return:
        """
        pass

    @abstractmethod
    def get_successors(self, vertex):
        """
        Get the successors of a given vertex.
        :param str vertex:
        :return:
        """
        pass

    @abstractmethod
    def get_all_vertices(self):
        """
        Returns a set containing all the vertices in the graph.
        :return:
        """
        pass






