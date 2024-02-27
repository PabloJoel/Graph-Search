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


@callback(
    Output('main-div', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_layout(n):
    if DashVisualizer.dash_show_flag and DashVisualizer.dash_show_flag_done:
        for elem in DashVisualizer.dash_elements:
            if isinstance(elem, cyto.Cytoscape):
                pass
                #DashVisualizer.dash_elements[1].layout['name'] = 'preset'
        DashVisualizer.dash_show_flag = False
        DashVisualizer.dash_show_flag_done = False

    if DashVisualizer.dash_show_flag:
        DashVisualizer.dash_show_flag_done = True

    return DashVisualizer.dash_elements

#todo ver si puedo pillar las posiciones de los nodos, setearlos y marcar el layout como preset
#todo meter la visualizacion de close, open y current


class DashVisualizer(Visualizer):
    """
    DashVisualizer is a type of visualizer that creates a Dash dashboard, where the graph is going to be displayed
    and updated.
    """
    dash_elements = list()
    dash_show_flag = False
    dash_show_flag_done = False
    dash_wait_flag = False

    def __init__(self):
        """
        This method loads the data and creates a server running Dash on localhost:8050, which displays the loaded graph.

        :param pd.DataFrame data: pandas DataFrame containing the graph details.
        """
        super().__init__()

        self.app = Dash(__name__)
        self.thread = threading.Thread(target=self.__run_dash)
        self.thread.start()  # Run the Dash server on the background

    def __generate_dash_graph(self, graph, current=None, open=list(), close=list()):
        """
        Internal method that converts a pandas dataframe (representing a Graph) into a list that can be ingested by
        Dash to create a visualization of the graph.

        :param Graph graph: graph object to visualize.
        :return:
        """
        self.vertices = set()
        graph_elements = graph.data.apply(self.__create_graph, weight_cols=graph.weight_cols, current=current,
                                          open=open, close=close, axis=1)
        graph_elements = [item for sublist in graph_elements for item in sublist]

        return cyto.Cytoscape(
            id=f'cytoscape-{len(DashVisualizer.dash_elements)}-nodes',
            elements=graph_elements,
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
                    'selector': '.open',
                    'style': {'background-color': 'green'}
                },
                {
                    'selector': '.close',
                    'style': {'background-color': 'red'}
                },
                {
                    'selector': '.current',
                    'style': {'background-color': 'yellow'}
                },
                {
                    'selector': '.unselected',
                    'style': {'background-color': 'blue'}
                },
            ],
            layout={'name': 'breadthfirst'},
            style={'width': '1400px', 'height': '1500px'}
        )

    def __create_graph(self, row, weight_cols, current=None, open=list(), close=list()):
        """
        Internal method that transforms the data from a single row of the dataframe into a list containing: the source
        vertex, the target vertex and the edge linking both vertices. Repeated vertices are not duplicated.

        :param pd.Series row: pandas Series containing a row from the data DataFrame.
        :return:
        """
        res = list()

        # Source vertex
        if row['source'] not in self.vertices:
            node_class = self.__get_node_class(node=row['source'], current=current, open=open, close=close)
            res.append({'data': {'id': row['source'], 'label': row['source']}, 'type': 'node', 'classes': node_class})    # Source vertex
            self.vertices.add(row['source'])

        # Target vertex
        if row['target'] not in self.vertices:
            node_class = self.__get_node_class(node=row['target'], current=current, open=open, close=close)
            res.append({'data': {'id': row['target'], 'label': row['target']}, 'type': 'node', 'classes': node_class})    # Target vertex
            self.vertices.add(row['target'])

        # Edge from Source to Target
        weight = '(' + ','.join([str(row[weight]) for weight in weight_cols]) + ')'
        res.append({'data': {'source': row['source'], 'target': row['target'], 'weight': weight}, 'type': 'edge'})          # Edge

        return res

    def __get_node_class(self, node, current, open, close):
        if node == current:
            return'current'
        elif node in open:
            return 'open'
        elif node in close:
            return'close'
        return 'unselected'

    def __generate_dash_button(self):
        return [
            self.__generate_dash_interval(),
            html.Button('Continue', id='update_button'),
            html.Div(id='container-button-basic', children='Press the button to continue the execution')
        ]

    def __generate_dash_interval(self):
        return dcc.Interval(id='interval-component', interval=1000, n_intervals=0)

    def __update_dash(self, elements):
        """
        Internal method used to update the Dash visualization.

        :param list elements: list of elements to be displayed on the Dash dashboard.
        :return:
        """
        self.app.layout = html.Div(id='main-div', children=elements)

    def __run_dash(self):
        """
        Internal method used to run the Dash server.

        :return:
        """
        self.app.run(debug=False)

    def wait(self, graph, current, open=list(), close=list()):
        DashVisualizer.dash_elements = list()
        DashVisualizer.dash_elements.extend(self.__generate_dash_button())
        DashVisualizer.dash_elements.append(self.__generate_dash_graph(graph, current=current, open=open, close=close))
        self.__update_dash(DashVisualizer.dash_elements)

        event_lock.wait()

    def show(self, graph):
        """
        This method updates the Dash dashboard to show the current state of the graph.
        :return:
        """

        if not (len(DashVisualizer.dash_elements) > 0 and isinstance(DashVisualizer.dash_elements[0], dcc.Interval)):
            DashVisualizer.dash_elements.append(self.__generate_dash_interval())

        if isinstance(graph, Graph):
            graph = [graph]

        for elem in graph:
            DashVisualizer.dash_elements.append(self.__generate_dash_graph(elem))

        self.__update_dash(DashVisualizer.dash_elements)

        DashVisualizer.dash_show_flag = True