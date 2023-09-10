import threading
import re
from dash import Dash, html
import dash_cytoscape as cyto

from Graph.Graph import Graph

#todo: check if there is an option to display the graph avoiding edges touching edges
#todo: increase arrow size and label size
#todo: documentation


class DashGrap(Graph):

    def __init__(self, data):
        super().__init__(data)
        self.elements = self.generate_dash_graph(self.data)

        self.app = Dash(__name__)
        self.update_dash(self.elements)

        threading.Thread(target=self.run_dash).start()

    def generate_dash_graph(self, data):
        self.vertices = set()
        elements = data.apply(self.create_graph, axis=1)
        elements = [item for sublist in elements for item in sublist]
        return elements

    def create_graph(self, row):
        res = list()
        if row['source'] not in self.vertices:
            res.append({'data': {'id': row['source'], 'label': row['source']}, 'type': 'node', 'classes': 'unselected'})    # Source vertex
            self.vertices.add(row['source'])
        if row['target'] not in self.vertices:
            res.append({'data': {'id': row['target'], 'label': row['target']}, 'type': 'node', 'classes': 'unselected'})    # Target vertex
            self.vertices.add(row['target'])

        pattern = re.compile('weight.*')
        weight_columns = list(filter(pattern.match, row.keys()))
        weight = '(' + ','.join([str(row[weight]) for weight in weight_columns]) + ')'
        res.append({'data': {'source': row['source'], 'target': row['target'], 'weight': weight}, 'type': 'edge'})          # Edge

        return res

    def update_dash(self, elements):
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

    def run_dash(self):
        self.app.run(debug=False)

    def show(self):
        self.elements.append({'data': {'source': 'n1', 'target': 'n2', 'weight': 1}, 'type': 'edge'})
        self.update_dash(self.elements)

