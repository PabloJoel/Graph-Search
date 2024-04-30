import copy

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer
from Heuristics.Random import Random
from Algorithms.Dijkstra import Dijkstra


class PULSE(Algorithm):
    """
    PULSE Algorithm fins (one-to-one) paths from a start node to an end node, while simultaneously minimizing two
    (conflicting) objective functions.
    """

    def __init__(self, graph: Graph, visualizer=ConsoleVisualizer()):
        """
        Creates the algorithm by using the input graph that contains the data, and by creating an empty Graph where the
        solution is going to be added later.
        The solution graph is created using the same parameters as the input graph, but empty.
        :param Graph graph: input graph containing the data.
        :param Visualizer visualizer: visualizer implementation to visualize the graphs. By default: ConsoleVisualizer.
        """

        super().__init__(graph, visualizer)

        # Algorithm Parameters
        self.check_solutions, self.labels, self.min_c_cost, self.min_t_cost = dict(), dict(), dict(), dict()
        self.start_vertex, self.end_vertex, self.nadir_point = None, None, None

    def run(self, start_vertex, end_vertex=None, show_by_step=False, show_end=False):
        """
        Runs the algorithm from start_vertex until there are no more vertices to explore or end_vertex has been explored.
        :param str start_vertex:
        :param str end_vertex:
        :return:
        """
        solution_template = Graph(
            data=pd.DataFrame(),
            source_col=self.graph.source_col,
            target_col=self.graph.target_col,
            weight_cols=self.graph.weight_cols,
            bidirectional=self.graph.bidirectional
        )

        all_vertices = self.graph.get_all_vertices()
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.check_solutions, self.labels, self.min_c_cost, self.min_t_cost = dict(), dict(), dict(), dict()
        self.nadir_point = None

        if start_vertex in all_vertices and end_vertex in all_vertices and start_vertex != end_vertex:
            self._initialization(end_vertex)
            self._pulse(start_vertex, 0, 0, tuple(), show_by_step)
            for path in self.check_solutions.keys():
                solution_path = solution_template.copy()
                self._backtrack_sol(path, solution_path)
                self.solution.add_solution(end_vertex, solution_path)

        self.metrics.end_execution()
        if self.solution.is_empty():
            print(f'Warning, could not find a path from {start_vertex} to {end_vertex}')

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution.get_all_solutions())

    def _initialization(self, end_vertex):
        self._create_inverse_graph(self.graph, end_vertex)

    def _create_inverse_graph(self, graph, end_vertex):
        inverse_graph = graph.get_inverse_graph()
        inverse_graph_c = inverse_graph
        inverse_graph_t = inverse_graph.copy()

        inverse_graph_c.weight_cols = [self.graph.weight_cols[0]]
        inverse_graph_t.weight_cols = [self.graph.weight_cols[1]]

        dijkstra_c = Dijkstra(inverse_graph_c)
        dijkstra_c.run(start_vertex=end_vertex)
        self.inverse_c_sol = dijkstra_c.solution
        c_graph = self.inverse_c_sol.get_solution('*')[0]
        c_graph.weight_cols = [self.graph.weight_cols[0], self.graph.weight_cols[1]]
        c_graph.data[self.graph.weight_cols[1]] = c_graph.data.apply(lambda data: self.graph.get_weight(data[self.graph.target_col], data[self.graph.source_col])[1], axis=1)

        dijkstra_t = Dijkstra(inverse_graph_t)
        dijkstra_t.run(start_vertex=end_vertex)
        self.inverse_t_sol = dijkstra_t.solution
        t_graph = self.inverse_t_sol.get_solution('*')[0]
        t_graph.weight_cols = [self.graph.weight_cols[0], self.graph.weight_cols[1]]
        t_graph.data[self.graph.weight_cols[0]] = t_graph.data.apply(lambda data: self.graph.get_weight(data[self.graph.target_col], data[self.graph.source_col])[0], axis=1)

        C = self.inverse_t_sol.get_solution(self.start_vertex)[0].get_path_cost(start=self.end_vertex, end=self.start_vertex)[0]
        T = self.inverse_c_sol.get_solution(self.start_vertex)[0].get_path_cost(start=self.end_vertex, end=self.start_vertex)[1]
        self.nadir_point = (C,T)

    def _pulse(self, current_vertex, cumulative_c, cumulative_t, current_path, show_by_step):
        self.metrics.add_explored_node()
        if current_vertex == self.end_vertex:
            self._pulse_end(current_vertex, cumulative_c, cumulative_t, current_path)
        else:
            if not self._isCyclic(current_vertex, current_path):
                if not self._checkNadirPoint(current_vertex, cumulative_c, cumulative_t):
                    if not self._checkEfficientSet(current_vertex, cumulative_c, cumulative_t):
                        if not self._checkLabels(current_vertex, cumulative_c, cumulative_t):

                            successors = self.graph.get_successors(current_vertex)
                            if show_by_step:
                                self.visualizer.wait(graph=self.graph, current=current_vertex, open=successors,
                                                     close=self.labels.keys())

                            self._store(current_vertex, cumulative_c, cumulative_t)
                            new_path = list(current_path)
                            new_path.append(current_vertex)
                            new_path = tuple(new_path)
                            for successor in successors:
                                successor_cost_c, successor_cost_t = self.graph.get_weight(current_vertex, successor)
                                self._pulse(successor, cumulative_c+successor_cost_c, cumulative_t+successor_cost_t, new_path, show_by_step)

    def _pulse_end(self, current_vertex, cumulative_c, cumulative_t, current_path):
        if not self._checkEfficientSet(current_vertex, cumulative_c, cumulative_t):
            new_path = list(current_path)
            new_path.append(current_vertex)
            new_path = tuple(new_path)
            self._updateEfficientSet(cumulative_c, cumulative_t, new_path)

    def _isCyclic(self, vertex, path):
        return vertex in path

    def _checkNadirPoint(self, vertex, cumulative_c, cumulative_t):
        try:
            if vertex in self.min_c_cost:
                c_min = self.min_c_cost[vertex]
            else:
                c_min = self.inverse_c_sol.get_solution(vertex)[0].get_path_cost(start=self.end_vertex, end=vertex)[0]
                self.min_c_cost[vertex] = c_min

            if vertex in self.min_t_cost:
                t_min = self.min_t_cost[vertex]
            else:
                t_min = self.inverse_t_sol.get_solution(vertex)[0].get_path_cost(start=self.end_vertex, end=vertex)[1]
                self.min_t_cost[vertex] = t_min

            C,T = self.nadir_point
        except Exception as ex:
            return True

        c_max = C - c_min
        t_max = T - t_min

        if cumulative_c > c_max or cumulative_t > t_max:
            return True
        else:
            return False

    def _checkEfficientSet(self, vertex, cumulative_c, cumulative_t):
        try:
            if vertex in self.min_c_cost:
                c_min = self.min_c_cost[vertex]
            else:
                c_min = self.inverse_c_sol.get_solution(vertex)[0].get_path_cost(start=self.end_vertex, end=vertex)[0]
                self.min_c_cost[vertex] = c_min

            if vertex in self.min_t_cost:
                t_min = self.min_t_cost[vertex]
            else:
                t_min = self.inverse_t_sol.get_solution(vertex)[0].get_path_cost(start=self.end_vertex, end=vertex)[1]
                self.min_t_cost[vertex] = t_min

        except Exception as ex:
            return True

        my_solution = (cumulative_c + c_min, cumulative_t + t_min)
        for solution in self.check_solutions.values():
            if self.is_dominated(my_solution, solution):
                return True
        return False

    def _updateEfficientSet(self, c, t, new_path):
        updated_x = dict()
        for path, costs in self.check_solutions.items():
            if not self.is_dominated(costs, (c,t)):
                updated_x.update({path: costs})
        updated_x.update({new_path: (c, t)})
        self.check_solutions = updated_x

    def _checkLabels(self, vertex, cumulative_c, cumulative_t):
        current_labels = self.labels.get(vertex, list())
        for cost in current_labels:
            if self.is_dominated((cumulative_c, cumulative_t), cost):
                return True
        return False

    def _store(self, vertex, cumulative_c, cumulative_t):
        new_sol = (cumulative_c, cumulative_t)
        current_labels = self.labels.get(vertex, list())
        if not self.is_dominated(new_sol, current_labels):
            current_labels.append(new_sol)
            self.labels[vertex] = self._get_nd_subset(current_labels)

    def is_dominated(self, costs1, costs2):
        """
        Returns True if costs1 is dominated by costs2.
        :param tuple or list costs1:
        :param tuple or list costs2:
        :return:
        """
        # Edge case: one or both of them is Infinity
        if (isinstance(costs1, tuple) or isinstance(costs1, list)) and costs2 == float('inf'):
            return False
        elif (isinstance(costs2, tuple) or isinstance(costs2, list)) and costs1 == float('inf'):
            return True
        elif costs1 == float('inf') and costs2 == float('inf'):
            return False
        elif len(costs2) == 0:
            return False
        elif len(costs1) == 0:
            return True

        if not isinstance(costs1, list):
            costs1 = [costs1]
        if not isinstance(costs2, list):
            costs2 = [costs2]

        for sublist2 in costs2:
            dominance = True
            for sublist1 in costs1:
                check_dm = self._check_dominance(sublist1, sublist2)
                if not check_dm:
                    dominance = False
            if dominance:
                return True
        return False

    def _check_dominance(self, costs1, costs2):
        if len(costs1) != len(costs2):
            raise ValueError(f"Error, both costs must have the same size, but cost1:{costs1} and cost2:{costs2} have different sizes")

        as_good = True
        is_better = False

        c1, t1 = costs1[0], costs1[1]
        c2, t2 = costs2[0], costs2[1]
        if c2 > c1 or t2 > t1:
            as_good = False  # List2 is worse than List1

        if c2 < c1 or t2 < t1:
            is_better = True  # List2 is better than Cost1

        return as_good and is_better

    def _get_nd_subset(self, elements):
        subset = list()
        for elem in elements:
            if not self.is_dominated(elem, elements):
                subset.append(elem)
        return subset

    def _substract_costs(self, list1, list2):
        if len(list1) != len(list2):
            raise ValueError(f"Cant substract {list1} and {list2} as they have different sizes.")

        res = list()
        for c1, c2 in zip(list1, list2):
            res.append(c1-c2)
        return res

    def _backtrack_sol(self, path, solution_path):
        for index in range(len(path)):
            current_vertex = path[index]
            if current_vertex == self.end_vertex:
                return

            next_vertex = path[index+1]
            weight = self.graph.get_weight(current_vertex, next_vertex)
            solution_path.add_edge(current_vertex, next_vertex, weights=weight)
