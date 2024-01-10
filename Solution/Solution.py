from Graphs.Graph import Graph


class Solution:

    def __init__(self):
        self._solutions = dict()

    def add_solution(self, vertex: str, solution: Graph):
        if vertex in self._solutions:
            self._solutions[vertex].append(solution)
        else:
            self._solutions[vertex] = [solution]

    def get_solution(self, vertex: str):
        if vertex in self._solutions:
            return self._solutions.get(vertex, list())
        elif '*' in self._solutions:
            return self._solutions.get('*', list())

    def get_all_solutions(self):
        return [subelem for elem in list(self._solutions.values()) for subelem in elem]
