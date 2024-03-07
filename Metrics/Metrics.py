import datetime as dt


class Metrics:
    def __init__(self):
        self.nodes_explored = 0
        self.start_datetime = None
        self.end_datetime = None
        self.execution_datetime = None
        self.execution_time = None

    def add_explored_node(self, node_amount=1):
        if self.start_datetime is None:
            self.start_datetime = dt.datetime.now()
        self.nodes_explored += node_amount

    def end_execution(self):
        self.end_datetime = dt.datetime.now()
        if self.start_datetime is None:
            self.execution_datetime = None
            self.execution_time = None
        else:
            self.execution_datetime = self.end_datetime - self.start_datetime
            self.execution_time = self.execution_datetime.total_seconds()

    def __str__(self):
        return f'Nodes explored: {self.nodes_explored}\nStart datetime: {self.start_datetime}\nEnd datetime: ' \
               f'{self.end_datetime}\nExecution time: {self.execution_datetime}\nExecution time (seconds): ' \
               f'{self.execution_time}'