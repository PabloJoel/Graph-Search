import re
import pandas as pd


class Graph:
    """
    This is the base class to represent a Graph.
    """

    def __init__(self, data, bidirectional=False):
        """
        This method loads the data that represents the Graph.
        :param boolean bidirectional: if True, all edges work both ways.
        :param pd.DataFrame data: pandas DataFrame containing the graph details.
        """
        self.data = data

        if bidirectional:
            weight_cols = list(filter(re.compile('weight').match, self.data.columns))
            bidirectional_df = pd.DataFrame()
            bidirectional_df['source'] = self.data['target']
            bidirectional_df['target'] = self.data['source']
            for weigth_col in weight_cols:
                bidirectional_df[weigth_col] = self.data[weigth_col]
            self.data = pd.concat([self.data, bidirectional_df])
            del bidirectional_df

        self.explored_nodes = set()

    def add_node(self, source, target, direction='unidirectional', weights=[]):
        data = {'source': [source], 'target': [target], 'direction': [direction]}
        for index, weight in enumerate(weights):
            data.update({f'weight_{index+1}': weight})
        node = pd.DataFrame(data=data)

        self.data = pd.concat([self.data, node])

    def is_explored(self, node):
        return node in self.explored_nodes

    def add_explored_node(self, node):
        self.explored_nodes.add(node)

    def get_weight(self, source, target):
        weight_cols = list(filter(re.compile('weight').match, self.data.columns))
        return self.data[self.data['source']==source][self.data['target']==target][weight_cols].to_dict('records')[0]

    def get_predecessors(self, node):
        """
        Get the predecessors of a given node.
        :param str node: a vertex
        :return:
        """
        return list(self.data[self.data['target'] == node]['source'])

    def get_successors(self, node):
        """
        Get the successors of a given node.
        :param str node: a vertex
        :return:
        """
        return list(self.data[self.data['source'] == node]['target'])

    def show(self):
        """
        This method prints in the console the current state of the Graph.
        :return:
        """
        print(self.data)


