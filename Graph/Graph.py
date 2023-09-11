

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

    def show(self):
        """
        This method prints in the console the current state of the Graph.
        :return:
        """
        print(self.data)


