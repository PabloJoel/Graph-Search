import threading
import re
import pandas as pd
from dash import Dash, html
import dash_cytoscape as cyto

from Graph.Graph import Graph

#todo: check if there is an option to display the graph avoiding edges touching edges
#todo: increase arrow size and label size


class DashGraph(Graph):
    """
    DashGraph is a subclass of Graph, which has a different visualization than its parent class.
    DashGraph creates a Dash dashboard, where the graph is going to be displayed and updated.
    """

    def __init__(self, data):
        """
        This method loads the data and creates a server running Dash on localhost:8050, which displays the loaded graph.

        :param pd.DataFrame data: pandas DataFrame containing the graph details.
        """
        super().__init__(data)
        self.dash_graph = self.__generate_dash_graph(self.data)   # Transform the graph dataframe to a Dash visualization

        self.app = Dash(__name__)
        self.__update_dash(self.dash_graph)   # Add the graph to the Dash dashboard

        threading.Thread(target=self.__run_dash).start()  # Run the Dash server on the background

    def __generate_dash_graph(self, data):
        """
        Internal method that converts a pandas dataframe (representing a Graph) into a list that can be ingested by
        Dash to create a visualization of the graph.

        :param pd.DataFrame data: pandas DataFrame containing the graph details.
        :return:
        """
        self.vertices = set()
        elements = data.apply(self.__create_graph, axis=1)
        elements = [item for sublist in elements for item in sublist]
        return elements

    def __create_graph(self, row):
        """
        Internal method that transforms the data from a single row of the dataframe into a list containing: the source
        vertex, the target vertex and the edge linking both vertices. Repeated vertices are not duplicated.

        :param pd.Series row: pandas Series containing a row from the data DataFrame.
        :return:
        """
        res = list()

        # Source vertex
        if row['source'] not in self.vertices:
            res.append({'data': {'id': row['source'], 'label': row['source']}, 'type': 'node', 'classes': 'unselected'})    # Source vertex
            self.vertices.add(row['source'])

        # Target vertex
        if row['target'] not in self.vertices:
            res.append({'data': {'id': row['target'], 'label': row['target']}, 'type': 'node', 'classes': 'unselected'})    # Target vertex
            self.vertices.add(row['target'])

        # Edge from Source to Target
        pattern = re.compile('weight.*')
        weight_columns = list(filter(pattern.match, row.keys()))
        weight = '(' + ','.join([str(row[weight]) for weight in weight_columns]) + ')'
        res.append({'data': {'source': row['source'], 'target': row['target'], 'weight': weight}, 'type': 'edge'})          # Edge

        return res

    def __update_dash(self, elements):
        """
        Internal method used to update the Dash visualization.

        :param list elements: list of elements to be displayed on the Dash dashboard.
        :return:
        """
        self.app.layout = html.Div([
            cyto.Cytoscape(
                id='cytoscape',
                elements=elements,
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {'label': 'data(id)'}
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            'label': 'data(weight)',
                            'target-arrow-shape': 'triangle'
                        }
                    },
                    {
                        'selector': '.selected',
                        'style': {'background-color': 'red'}
                    },
                    {
                        'selector': '.unselected',
                        'style': {'background-color': 'blue'}
                    },
                ],
                layout={'name': 'breadthfirst'},
                style={'width': '1400px', 'height': '1500px'}
            )
        ])

    def __run_dash(self):
        """
        Internal method used to run the Dash server.

        :return:
        """
        self.app.run(debug=False)

    def show(self):
        """
        This method updates the Dash dashboard to show the current state of the graph.
        :return:
        """
        self.dash_graph = self.__generate_dash_graph(self.data)
        self.__update_dash(self.dash_graph)

