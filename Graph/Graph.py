

class Graph:
    """
    Dash is the base class to represent a Graph.
    """

    def __init__(self, data):
        """
        This method loads the data that represents the Graph.

        :param pd.DataFrame data: pandas DataFrame containing the graph details.
        """
        self.data = data

    def get_predecessors(self, node):
        """
        Get the predecessors of a given node.
        :return:
        """
        nodes = self.data.loc[self.data['target'].str.contains(node) == True]
        return self.data.loc[self.data['source'].isin(nodes['source'])].reset_index(drop=True)
    def get_successors(self, node):
        """
        Get the successors of a given node.
        :param node:
        :return:
        """
        nodes = self.data.loc[self.data['source'].str.contains(node) == True]
        return self.data.loc[self.data['source'].isin(nodes['target'])].reset_index(drop=True)

    def show(self):
        """
        This method prints in the console the current state of the Graph.
        :return:
        """
        print(self.data)


