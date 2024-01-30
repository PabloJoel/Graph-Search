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
        self.weight_cols = weight_cols if isinstance(weight_cols, list) or isinstance(weight_cols, set) else [weight_cols]
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

    def add_edge(self, source, target, weights=list()):
        """
        Add an edge from source to target to the graph. Optionally, a dict of weights can be added to the edge.
        :param str source: source vertex.
        :param str target:  target vertex.
        :param list weights: dict where keys are weight column names and values are the actual weights.
        :return:
        """
        data = {self.source_col: source, self.target_col: target}

        # Add weights
        if len(self.weight_cols) != len(weights):
            raise ValueError(f'The weights columns are {self.weight_cols}, but the weights added were {weights}, '
                             f'which doesnt align with the number of columns')
        for weight_col, weight_value in zip(self.weight_cols, weights):
            data.update({weight_col: weight_value})

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

    def remove_edge(self, source, target):
        """
        Remove the edge between source and target vertices, if it exists.
        :param str source: source vertex.
        :param str target:  target vertex.
        :return:
        """
        if not self.data.empty:
            self.data.drop(self.data[(self.data[self.source_col] == source) & (self.data[self.target_col] == target)].index, inplace=True)
            if self.bidirectional:
                self.data.drop(self.data[(self.data[self.source_col] == target) & (self.data[self.target_col] == source)].index, inplace=True)

    def get_weight(self, source, target):
        """
        Returns the weights of the edge between source vertex and target vertex. If there is no connection, returns an
        empty dictionary.
        :param str source: source vertex of the edge.
        :param str target: target vertex of the edge.
        :return:
        """
        if len(self.weight_cols) == 0:
            return list()

        source = self.data[self.data[self.source_col]==source]
        source_target = source[source[self.target_col]==target]
        if source_target.empty:
            return list()
        else:
            return list(source_target[self.weight_cols].iloc[0])

    def get_predecessors(self, vertex):
        """
        Get the predecessors of a given vertex.
        :param str vertex:
        :return:
        """
        try:
            return list(self.data[self.data[self.target_col] == vertex][self.source_col])
        except:
            return list()

    def get_successors(self, vertex):
        """
        Get the successors of a given vertex.
        :param str vertex:
        :return:
        """
        try:
            return list(self.data[self.data[self.source_col] == vertex][self.target_col])
        except:
            return list()

    def get_all_vertices(self):
        """
        Returns a set containing all the vertices in the graph.
        :return:
        """
        try:
            vertices = set(self.data[self.source_col])          # Source vertices
            vertices.update(self.data[self.target_col])         # Target vertices
            return vertices
        except:
            return set()

    def get_path_cost(self, start, end):
        """
        Returns the cost of traversing from start to end.
        :param start: start vertex
        :param end: end vertex
        :return:
        """
        cost = [0 for weight in self.weight_cols]
        node = end
        while node != start:
            predecessor = self.get_predecessors(node)[0]
            weight = self.get_weight(predecessor, node)
            for index, value in enumerate(weight):
                cost[index] += value
            node = predecessor
        return cost

    def get_path_uninformed(self, start, end):
        """
        Returns the path between start and end, by traversing the graph from end to start.
        :param start: start vertex
        :param end: end vertex
        :return:
        """
        path = Graph(pd.DataFrame(), source_col=self.source_col, target_col=self.target_col,
                     weight_cols=self.weight_cols, bidirectional=False)
        node = end
        while node != start:
            predecessor = self.get_predecessors(node)[0]
            weight = self.get_weight(predecessor, node)
            path.add_edge(source=predecessor, target=node, weights=weight)
            node = predecessor
        return path

    def get_path_informed(self, start, end, prev):
        """
        This method returns a Graph representing the path between start and end vertices. To achieve this, a dictionary
        "prev" must be passed where keys are vertices and their values are the vertex that proceeds them. Only a single
        vertex can precede a vertex.
        :param start:
        :param end:
        :param prev:
        :return:
        """
        path = Graph(pd.DataFrame(), source_col=self.source_col, target_col=self.target_col,
                     weight_cols=self.weight_cols, bidirectional=False)
        path_ready = False
        current = end
        while not path_ready:
            source = prev[current]
            target = current
            cost = self.get_weight(source=source, target=target)
            path.add_edge(source=source, target=target, weights=cost)

            if source == start:
                path_ready = True
            else:
                current = source
        return path

    def get_inverse_graph(self):
        """
        Returns a copy of the graph but the edges have been inverted.
        :return:
        """
        inverse_graph = pd.DataFrame()
        if not self.data.empty:
            inverse_graph[self.source_col] = self.data[self.target_col]
            inverse_graph[self.target_col] = self.data[self.source_col]
            for weigth_col in self.weight_cols:
                inverse_graph[weigth_col] = self.data[weigth_col]
        return Graph(inverse_graph, source_col=self.source_col, target_col=self.target_col,
                     weight_cols=self.weight_cols, bidirectional=self.bidirectional)

    def copy(self):
        """
        Returns a copy of the graph.
        :return:
        """
        copy = Graph(self.data.copy(deep=True), source_col=self.source_col, target_col=self.target_col, weight_cols=self.weight_cols,
                     bidirectional=self.bidirectional)
        return copy

    def show(self):
        """
        This method prints in the console the current state of the Graph.
        :return:
        """
        print(self.data)


