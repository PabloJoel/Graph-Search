from Graphs.Graph import Graph


class Solution:

    def __init__(self):
        self._solutions = dict()

    def add_solution(self, vertex: str, solution: Graph):
        if vertex in self._solutions:
            self._solutions[vertex].append(solution)
        else:
            self.set_solution(vertex, solution)

    def set_solution(self, vertex: str, solution: Graph):
        self._solutions[vertex] = [solution]

    def get_solution(self, vertex: str):
        if vertex in self._solutions:
            return self._solutions.get(vertex, list())
        elif '*' in self._solutions:
            return self._solutions.get('*', list())

    def get_solution_cost(self, vertex_start, vertex_objective):
        sol = list()
        for solution in self.get_solution(vertex_objective):
            sol.append(solution.get_path_cost(start=vertex_start, end=vertex_objective))
        return sol

    def get_solution_path(self, vertex_objective):
        return self.get_solution(vertex_objective)

    def get_min_solution_cost(self, vertex_start):
        compressed_list = [self.get_solution_cost(vertex_start, objective) for objective in self._solutions.keys()]
        res = [subelem for elem in compressed_list for subelem in elem]
        if len(res) > 0:
            return min(res)
        else:
            return list()

    def get_all_solutions(self):
        return [subelem for elem in list(self._solutions.values()) for subelem in elem]

    def is_empty(self):
        return len(self._solutions) == 0
