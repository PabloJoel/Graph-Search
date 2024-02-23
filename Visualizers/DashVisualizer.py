import threading
import pandas as pd
import dash_cytoscape as cyto
from dash import Dash, dcc, html, Input, Output, State, callback

from Graphs.Graph import Graph
from Visualizers.Visualizer import Visualizer


# Global Object to stop and start the execution of the process
event_lock = threading.Event()


@callback(
    Output('container-button-basic', 'children'),
    Input('update_button', 'n_clicks'),
    prevent_initial_call=True
)
def update_button(n_clicks):
    event_lock.set()
    event_lock.clear()
    return 'Executing the algorithm...'


class DashVisualizer(Visualizer):
    """
    DashVisualizer is a type of visualizer that creates a Dash dashboard, where the graph is going to be displayed
    and updated.
    """

    def __init__(self):
        """
        This method loads the data and creates a server running Dash on localhost:8050, which displays the loaded graph.

        :param pd.DataFrame data: pandas DataFrame containing the graph details.
        """
        super().__init__()
        self.elements = list()

        self.app = Dash(__name__)
        self.thread = threading.Thread(target=self.__run_dash)
        self.thread.start()  # Run the Dash server on the background

    def __generate_dash_graph(self, graph):
        """
        Internal method that converts a pandas dataframe (representing a Graph) into a list that can be ingested by
        Dash to create a visualization of the graph.

        :param Graph graph: graph object to visualize.
        :return:
        """
        self.vertices = set()
        elements = graph.data.apply(self.__create_graph, weight_cols=graph.weight_cols, axis=1)
        elements = [item for sublist in elements for item in sublist]

        return cyto.Cytoscape(
            id=f'cytoscape-{len(self.elements)}-nodes',
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

    def __create_graph(self, row, weight_cols):
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
        weight = '(' + ','.join([str(row[weight]) for weight in weight_cols]) + ')'
        res.append({'data': {'source': row['source'], 'target': row['target'], 'weight': weight}, 'type': 'edge'})          # Edge

        return res

    def __generate_dash_button(self):
        return [html.Button('Continue', id='update_button'),
                html.Div(id='container-button-basic', children='Press the button to continue the execution')]

    def __generate_dash_graph_step(self, graph, current, open=list(), close=list()):
        """
        Internal method that converts a pandas dataframe (representing a Graph) into a list that can be ingested by
        Dash to create a visualization of the graph.

        :param Graph graph: graph object to visualize.
        :return:
        """
        self.vertices = set()
        elements = graph.data.apply(self.__create_graph_step, current=current, open=open, close=close, weight_cols=graph.weight_cols, axis=1)
        elements = [item for sublist in elements for item in sublist]
        return elements

    def __create_graph_step(self, row, current, open, close, weight_cols):
        """
        Internal method that transforms the data from a single row of the dataframe into a list containing: the source
        vertex, the target vertex and the edge linking both vertices. Repeated vertices are not duplicated.

        :param pd.Series row: pandas Series containing a row from the data DataFrame.
        :return:
        """#todo add something so that i can modify the colors later with css
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
        weight = '(' + ','.join([str(row[weight]) for weight in weight_cols]) + ')'
        res.append({'data': {'source': row['source'], 'target': row['target'], 'weight': weight}, 'type': 'edge'})          # Edge

        return res

    def __update_dash(self, elements):
        """
        Internal method used to update the Dash visualization.

        :param list elements: list of elements to be displayed on the Dash dashboard.
        :return:
        """
        self.app.layout = html.Div(elements)

    def __run_dash(self):
        """
        Internal method used to run the Dash server.

        :return:
        """
        self.app.run(debug=False)

    def wait(self, graph, current, open=list(), close=list()):
        self.elements = list()
        self.elements.extend(self.__generate_dash_button())
        self.elements.append(self.__generate_dash_graph(graph))
        self.__update_dash(self.elements)

        event_lock.wait()

    def show(self, graph):
        """
        This method updates the Dash dashboard to show the current state of the graph.
        :return:
        """
        if isinstance(graph, Graph):
            graph = [graph]

        for elem in graph:
            self.elements.append(self.__generate_dash_graph(elem))

        self.__update_dash(self.elements)
