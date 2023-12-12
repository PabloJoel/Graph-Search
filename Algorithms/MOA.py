import copy

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer
from Heuristics.Random import Random


class MOA(Algorithm):
    """
    MOA* algorithm
    """

    def __init__(self, graph: Graph, visualizer=ConsoleVisualizer(), heuristic=Random):
        """
        Creates the algorithm by using the input graph that contains the data, and by creating an empty Graph where the
        solution is going to be added later.
        The solution graph is created using the same parameters as the input graph, but empty.
        :param Graph graph: input graph containing the data.
        :param Visualizer visualizer: visualizer implementation to visualize the graphs. By default: ConsoleVisualizer.
        :param heuristic: heuristic function to be used. By default: BFS Heuristic.
        """
        solution = Graph(
            data=pd.DataFrame(),
            source_col=graph.source_col,
            target_col=graph.target_col,
            weight_cols=graph.weight_cols,
            bidirectional=graph.bidirectional
        )
        super().__init__(graph, solution, visualizer)
        self.heuristic = heuristic(graph)

    def step(self):
        """
        Run one step of the algorithm.
        :return:
        """
        pass

    def run(self, start_vertex, end_vertices=None, show_by_step=False, show_end=False):
        """
        Runs the algorithm from start_vertex until there are no more vertices to explore or end_vertex has been explored.
        :param str start_vertex:
        :param str or list end_vertices:
        :return:
        """
        if end_vertices is not None and isinstance(end_vertices, list):
            end_vertices = set(end_vertices)
        elif end_vertices is not None and not isinstance(end_vertices, set):
            end_vertices = {end_vertices}

        all_vertices = self.graph.get_all_vertices()
        finished = False
        if start_vertex in all_vertices and len(end_vertices.intersection(all_vertices)) != 0 \
                and end_vertices != {start_vertex}:#todo que ocurre si start=s y end=s,y1,y2??
            open = {start_vertex}
            closed = set()
            solution_costs, label = dict(), dict()

            h = {start_vertex: self._get_nd_successors(start_vertex)}#todo do a correct heuristic
            g = {vertex: [float("inf")] if vertex != start_vertex else [] for vertex in all_vertices}
            f = {vertex: [float("inf")] if vertex != start_vertex else h[start_vertex] for vertex in all_vertices}

            while not finished:
                # Step 1: Create ND (nodes from OPEN that are not dominated by SOLUTIONS or OPEN)
                nd = copy.deepcopy(open)
                for vertex in open:
                    cost = f[vertex]
                    removed = False

                    i = 0
                    compare_costs = list(solution_costs.values())       # Compare against the solutions
                    while i < len(solution_costs) and not removed:
                        removed = self.is_dominated(cost, compare_costs[i])
                        i += 1

                    for compare_vertex in open:
                        removed = self.is_dominated(cost, f[compare_vertex])    # Compare against the open vertices
                        if removed:
                            break

                    if removed:
                        nd.remove(vertex)

                # Step 2: Terminate or Select a vertex for expansion
                if len(nd) == 0:
                    # Step 2.1: Pick a solution and finish
                    solutions = list()
                    for solution, costs in solution_costs.items():
                        for cost in costs:
                            solution_path = self.solution.copy()
                            self._backtrack_sol(g=g, vertex=solution, accrued_cost=cost, solution_path=solution_path, start_vertex=start_vertex)
                            solutions.append(solution_path)
                    self.solution = solutions#todo multiple solutions
                    finished = True
                    break
                else:
                    pass
                    # Step 2.2: Get the best vertex using a problem specific heuristic
                    goals_nd = [elem for elem in nd if elem in end_vertices]
                    if len(goals_nd) == 0:
                        n = self.heuristic.calculate(nd)
                    else:
                        n = self.heuristic.calculate(goals_nd)

                    open.remove(n)
                    closed.add(n)

                if n in end_vertices:
                    # Step 4: Identify solution
                    values = list(solution_costs.values())
                    if len(values) > 0:
                        values = [subelem for elem in list(solution_costs.values()) for subelem in elem]
                    for my_cost in f[n]:
                        if not self.is_dominated(my_cost, values):
                            if n in solution_costs:
                                solution_costs[n].append(my_cost)
                            else:
                                solution_costs.update({n: [my_cost]})
                else:
                    # Step 5: Expand n and examine successors
                    successors = self.graph.get_successors(n)
                    if len(successors) > 0:
                        for successor in successors:
                            my_cost = self._add_costs(self.graph.get_weight(n, successor), g[n])

                            if successor not in open and successor not in closed:   # Newly generated vertex

                                if (n,successor) not in label:
                                    label[(n, successor)] = my_cost
                                else:
                                    is_dominated = False
                                    for cost in label[(n, successor)]:
                                        if self.is_dominated(my_cost, cost):
                                            is_dominated = True
                                    if not is_dominated:
                                        my_labels = label[(n, successor)]
                                        for cost in label[(n, successor)]:
                                            if self.is_dominated(cost, my_cost):
                                                my_labels.remove(cost)

                                g[successor] = copy.deepcopy(label[(n, successor)])

                                if successor not in h:
                                    h[successor] = self._get_nd_successors(successor)

                                f[successor] = self._add_costs(g[successor], h[successor])

                                open.add(successor)
                            else:   # Previously generated vertex
                                if (n,successor) in label:
                                    is_dominated = False
                                    for cost in label[(n,successor)]:
                                        if self.is_dominated(my_cost, cost):
                                            is_dominated = True

                                    if not is_dominated:
                                        my_labels = label[(n,successor)]
                                        for cost in label[(n,successor)]:
                                            if self.is_dominated(cost, my_cost):
                                                my_labels.remove(cost)
                                        my_labels.append(my_cost)

                                        if successor in closed:
                                            closed.remove(successor)
                                            open.add(successor)
                                else:
                                    label[(n, successor)] = my_cost

                                for cost in my_cost:
                                    if not self.is_dominated(cost, g[successor]):
                                        g[successor].append(cost)

                                if successor not in h:
                                    h[successor] = self._get_nd_successors(successor)

                                f[successor] = self._get_non_dm_subset(self._add_costs(g[successor], h[successor]))

        if not finished and end_vertices is not None:
            print(f'Warning, could not find a path from {start_vertex} to {end_vertices}')
            self.solution.data = pd.DataFrame()

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution)

    def is_dominated(self, costs1, costs2):
        """
        Returns True if costs1 is dominated by costs2.
        :param list costs1:
        :param list costs2:
        :return:
        """
        # Edge case: one or both of them is Infinity
        if isinstance(costs1, list) and costs2 == float('inf'):
            return False
        elif isinstance(costs2, list) and costs1 == float('inf'):
            return True
        elif costs1 == float('inf') and costs2 == float('inf'):
            return False
        elif len(costs2) == 0:
            return False
        elif len(costs1) == 0:
            return True

        if not isinstance(costs1[0], list):
            costs1 = [costs1]
        if not isinstance(costs2[0], list):
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

    def _check_dominance(self, list1, list2):
        as_good = True
        is_better = False
        for cost1, cost2 in zip(list1, list2):
            if cost2 > cost1:
                as_good = False     # List2 is worse than Cost1
            elif cost2 < cost1:
                is_better = True    # List2 is better than Cost1

        return as_good and is_better

    def _get_nd_successors(self, vertex):
        """
        Return the set of successors from vertex that are non dominated between each other.
        :param vertex:
        :return:
        """
        vertices = {successor: self.graph.get_weight(vertex, successor) for successor in
                    self.graph.get_successors(vertex)}

        nd = list()

        for vertex, weight1 in vertices.items():
            dominated = False
            for weight2 in vertices.values():
                if self.is_dominated(weight1, weight2):
                    dominated = True
            if not dominated and weight1 not in nd:
                nd.append(weight1)

        return nd

    def _get_non_dm_subset(self, elements):
        subset = list()
        for elem in elements:
            if not self.is_dominated(elem, elements):
                subset.append(elem)
        return subset

    def _add_costs(self, costs1, costs2):
        # Transform both to list of lists
        if len(costs1) == 0 or not isinstance(costs1[0], list):
            costs1 = [costs1]
        if len(costs2) == 0 or not isinstance(costs2[0], list):
            costs2 = [costs2]

        if len(costs1[0]) == 0:
            return costs2
        elif len(costs2[0]) == 0:
            return costs1

        res = list()
        for c1 in costs1:
            for c2 in costs2:
                res.append(self._add_lists(c1,c2))
        return res

    def _add_lists(self, list1, list2):
        if len(list1) != len(list2):
            raise ValueError(f"Cant add {list1} and {list2} as they have different sizes.")

        res = list()
        for c1, c2 in zip(list1, list2):
            res.append(c1+c2)
        return res

    def _asubstract_costs(self, costs1, costs2):
        # Transform both to list of lists
        if len(costs1) == 0 or not isinstance(costs1[0], list):
            costs1 = [costs1]
        if len(costs2) == 0 or not isinstance(costs2[0], list):
            costs2 = [costs2]

        if len(costs1[0]) == 0:
            return costs2
        elif len(costs2[0]) == 0:
            return costs1

        res = list()
        for c1 in costs1:
            for c2 in costs2:
                res.append(self._substract_lists(c1,c2))
        return res

    def _substract_lists(self, list1, list2):
        if len(list1) != len(list2):
            raise ValueError(f"Cant substract {list1} and {list2} as they have different sizes.")

        res = list()
        for c1, c2 in zip(list1, list2):
            res.append(c1-c2)
        return res

    def _backtrack_sol(self, g, vertex, accrued_cost, solution_path, start_vertex):
        predecessors = self.graph.get_predecessors(vertex)
        for predecessor in predecessors:
            weight = self.graph.get_weight(predecessor, vertex)
            substraction = self._substract_lists(accrued_cost, weight)
            if substraction in g[predecessor]:
                solution_path.add_edge(predecessor, vertex, weights=weight)
                self._backtrack_sol(g, predecessor, substraction, solution_path, start_vertex)
                return
            elif predecessor == start_vertex:
                solution_path.add_edge(predecessor, vertex, weights=weight)
                return




