import re
import pandas as pd


class Graph:
    """
    This is the base class to represent a Graph.
    """

    def __init__(self, data, source_col='source', target_col='target', weight_cols=list(), bidirectional=False):
        """
        This method loads the data that represents the Graph.
        :param pd.DataFrame data: pandas DataFrame containing the graph details.
        :param str source_col: column name for the source vertices.
        :param str target_col: column name for the target vertices.
        :param list weight_cols: list of columns names for the vertices weights.
        :param boolean bidirectional: if True, all edges work both ways.
        """
        self.data = data
        self.source_col = source_col
        self.target_col = target_col
        self.weight_cols = weight_cols
        self.bidirectional = bidirectional

        if bidirectional and not data.empty:
            bidirectional_df = pd.DataFrame()
            bidirectional_df[self.source_col] = self.data[self.target_col]
            bidirectional_df[self.target_col] = self.data[self.source_col]
            for weigth_col in self.weight_cols:
                bidirectional_df[weigth_col] = self.data[weigth_col]
            self.data = pd.concat([self.data, bidirectional_df])
            self.data.reset_index(drop=True, inplace=True)
            del bidirectional_df

        self.explored_nodes = set()

    def add_vertex(self, source, target, weights=dict()):
        """
        Add a vertex to the graph.
        :param str source: source vertex.
        :param str target:  target vertex.
        :param dict weights: dict where keys are weight column names and values are the actual weights.
        :return:
        """
        data = {self.source_col: source, self.target_col: target}

        # Add weights
        for weight_col in self.weight_cols:
            if weight_col in weights:
                data.update({weight_col: weights[weight_col]})

        # Duplicate edges if bidirectional
        if self.bidirectional:
            bidirectional_data = data.copy()
            bidirectional_data.update({self.source_col: data[self.target_col], self.target_col: data[self.source_col]})
            data = [data, bidirectional_data]
        else:
            data = [data]
        node = pd.DataFrame(data=data)

        self.data = pd.concat([self.data, node])
        self.data.reset_index(drop=True, inplace=True)

    def is_explored(self, vertex):
        """
        Returns True if the vertex has been marked as explored, otherwise False.
        :param str vertex: vertex to be checked.
        :return:
        """
        return vertex in self.explored_nodes

    def add_explored_vertex(self, vertex):
        """
        Marks a vertex as explored.
        :param str vertex: vertex to be marked.
        :return:
        """
        self.explored_nodes.add(vertex)

    def get_weight(self, source, target):
        """
        Returns the weights of the edge between source vertex and target vertex.
        :param str source: source vertex of the edge.
        :param str target: target vertex of the edge.
        :return:
        """
        source = self.data[self.data[self.source_col]==source]
        source_target = source[source[self.target_col]==target]
        return source_target[self.weight_cols].to_dict('records')[0]

    def get_predecessors(self, vertex):
        """
        Get the predecessors of a given vertex.
        :param str vertex:
        :return:
        """
        return list(self.data[self.data[self.target_col] == vertex][self.source_col])

    def get_successors(self, vertex):
        """
        Get the successors of a given vertex.
        :param str vertex:
        :return:
        """
        return list(self.data[self.data[self.source_col] == vertex][self.target_col])

    def show(self):
        """
        This method prints in the console the current state of the Graph.
        :return:
        """
        print(self.data)


