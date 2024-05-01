from Graphs.Graph import Graph


class Solution:

    def __init__(self):
        self._solutions = dict()

    def add_solution(self, vertex: str, solution: Graph):
        """
        Add a solution graph to the vertex.
        :param vertex:
        :param solution:
        :return:
        """
        if vertex in self._solutions:
            self._solutions[vertex].append(solution)
        else:
            self.set_solution(vertex, solution)

    def set_solution(self, vertex: str, solution: Graph):
        """
        Set a specific solution to a vertex, replacing it in case it is already occupied.
        :param vertex:
        :param solution:
        :return:
        """
        self._solutions[vertex] = [solution]

    def get_solution(self, vertex: str):
        """
        Return the solution graph for a given vertex.
        :param vertex:
        :return:
        """
        if vertex in self._solutions:
            return self._solutions.get(vertex, list())
        elif '*' in self._solutions:
            return self._solutions.get('*', list())

    def get_solution_cost(self, vertex_start, vertex_objective):
        """
        Returns a list containing the costs of the solutions between vertex_start and vertex_objective.
        :param vertex_start:
        :param vertex_objective:
        :return:
        """
        sol = list()
        for solution in self.get_solution(vertex_objective):
            sol.append(solution.get_path_cost(start=vertex_start, end=vertex_objective))
        return sol

    def get_solution_path(self, vertex_objective):
        """
        Returns the solution path for a given vertex.
        :param vertex_objective:
        :return:
        """
        return self.get_solution(vertex_objective)

    def get_min_solution_cost(self, vertex_start):
        """
        Returns the minimun cost among the solutions from vertex_start.
        :param vertex_start:
        :return:
        """
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
