import copy

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer
from Heuristics.Random import Random


class NAMOA(Algorithm):
    """
    NAMOA* algorithm
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
                and end_vertices != {start_vertex}:
            h = {start_vertex: self.heuristic.calculate(start_vertex)}
            gclose = dict()
            gopen = {vertex: [float("inf")] if vertex != start_vertex else [] for vertex in all_vertices}
            f = {vertex: [float("inf")] if vertex != start_vertex else h[start_vertex] for vertex in all_vertices}

            open = [(start_vertex, gopen[start_vertex], f[start_vertex])]
            goaln, costs, costs_vertex = set(), list(), dict()
            label = dict()

            while not finished:
                # Step 2: Check Termination
                if len(open) == 0:
                    solutions = list()
                    for vertex, costs in costs_vertex.items():
                        for cost in costs:
                            solution_path = self.solution.copy()
                            self._backtrack_sol(label=label, vertex=vertex, accrued_cost=cost, solution_path=solution_path,
                                                start_vertex=start_vertex)
                            solutions.append(solution_path)
                    self.solution = solutions
                    finished = True
                    break

                # Step 3: Path Selection
                all_fopen = [fvertex for vertex,gvertex,fvertex in open]
                chosen_vertex, chosen_gvertex, chosen_fvertex = None, None, None
                for elem in open:
                    vertex, gvertex, fvertex = elem
                    if not self._is_dominated_by_list(fvertex, all_fopen):
                        chosen_vertex = vertex
                        chosen_gvertex = gvertex
                        open.remove(elem)
                        if chosen_vertex in gclose:
                            gclose[chosen_vertex].extend(copy.deepcopy(chosen_gvertex))
                        else:
                            gclose[chosen_vertex] = copy.deepcopy(chosen_gvertex)

                        if chosen_vertex in gopen and len(chosen_gvertex) > 0:
                            for g_elem in chosen_gvertex:
                                if g_elem in gopen[chosen_vertex]:
                                    gopen[chosen_vertex].remove(copy.deepcopy(g_elem))

                        break

                if chosen_vertex in end_vertices:  # Step 4: Solution Recording
                    goaln.add(chosen_vertex)
                    costs.extend(copy.deepcopy(chosen_gvertex))
                    if chosen_vertex in costs_vertex:
                        costs_vertex[chosen_vertex].extend(copy.deepcopy(chosen_gvertex))
                    else:
                        costs_vertex[chosen_vertex] = copy.deepcopy(chosen_gvertex)

                    new_open = list()
                    for elem in open:
                        vertex, gvertex, fvertex = elem
                        new_fvertex = self._sublist_nondominated_single(fvertex, chosen_gvertex)
                        if len(new_fvertex) > 0:
                            new_open.append((vertex, gvertex, new_fvertex))
                    open = new_open
                else:   # Step 5: Path Expansion
                    for successor in self.graph.get_successors(chosen_vertex):
                        gsucc = self._add_costs(self.graph.get_weight(chosen_vertex, successor), chosen_gvertex)   # Step A:

                        all_verticesopen = [vertex for vertex,gvertex,fvertex in open]

                        if successor not in all_verticesopen and successor not in gclose.keys():    # Step B:

                            if successor not in h:
                                h[successor] = self.heuristic.calculate(successor)

                            # Step 5.1:
                            fsucc = list()
                            for elem in self._add_costs(gsucc, h[successor]):
                                if not self.is_dominated(elem, costs):
                                    fsucc.append(elem)
                            f[successor] = fsucc

                            # Step 5.2:
                            if len(fsucc) > 0:
                                open.append((successor, gsucc, fsucc))
                                if successor in gopen and float("inf") not in gopen[successor]:
                                    gopen[successor].extend(copy.deepcopy(gsucc))
                                else:
                                    gopen[successor] = copy.deepcopy(gsucc)
                                label[(chosen_vertex,successor)] = copy.deepcopy(gsucc)
                        elif self._in_gopen_or_gclose(gsucc, gopen, gclose, successor):
                                label[(chosen_vertex,successor)] = copy.deepcopy(gsucc)
                        elif not self.is_dominated(gsucc, gopen.get(successor, list())) and not self.is_dominated(gsucc, gclose.get(successor, list())):
                            if successor in gopen:
                                gopen[successor] = self._sublist_nondominated(gopen.get(successor, list()), gsucc, open, successor, fsucc)

                            if successor in gclose:
                                gclose[successor] = self._sublist_nondominated(gclose.get(successor, list()), gsucc, open, successor, fsucc)

                            if successor not in h:
                                h[successor] = self.heuristic.calculate(successor)

                            # Step 5.1:
                            fsucc = list()
                            for elem in self._add_costs(gsucc, h[successor]):
                                if not self.is_dominated(elem, costs):
                                    fsucc.append(elem)
                            f[successor] = fsucc
                            if len(fsucc) > 0:
                                open.append((successor, gsucc, fsucc))
                                if successor in gopen and float("inf") not in gopen[successor]:
                                    gopen[successor].extend(copy.deepcopy(gsucc))
                                else:
                                    gopen[successor] = copy.deepcopy(gsucc)
                                label[(chosen_vertex, successor)] = copy.deepcopy(gsucc)

        if not finished and end_vertices is not None:
            print(f'Warning, could not find a path from {start_vertex} to {end_vertices}')
            self.solution.data = pd.DataFrame()

        if isinstance(self.solution, Graph):
            self.solution = [self.solution]

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution)

    def _in_gopen_or_gclose(self, gsucc, gopen, gclose, successor):
        for elem in gsucc:
            if elem in gopen.get(successor, list()) or gsucc in gclose.get(successor, list()):
                return True
        return False

    def _is_dominated_by_list(self, elem, compare):
        """
        Returns True if any element in compare dominates elem.
        """
        for compare_elem in compare:
            if self.is_dominated(elem, compare_elem):
                return True
        return False

    def _sublist_nondominated_single(self, listinput, elemcompare):
        """
        Removes any element from listinput that is dominated by listcompare. Returns the subset.
        :param listinput:
        :param listcompare:
        :return:
        """
        res = list()
        for elem in listinput:
            if not self.is_dominated(elem, elemcompare):
                res.append(elem)
        return res

    def _sublist_nondominated(self, listinput, listcompare, open, succ, fsucc):
        """
        Removes any element from listinput that is dominated by listcompare. Returns the subset.
        :param listinput:
        :param listcompare:
        :return:
        """
        res = list()
        for elem in listinput:
            if not self.is_dominated(elem, listcompare):
                res.append(elem)
            elif (succ,elem,fsucc) in open:
                open.remove((succ,elem,fsucc))
        return res

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

    def _substract_lists(self, list1, list2):
        if len(list1) != len(list2):
            raise ValueError(f"Cant substract {list1} and {list2} as they have different sizes.")

        res = list()
        for c1, c2 in zip(list1, list2):
            res.append(c1-c2)
        return res

    def _backtrack_sol(self, label, vertex, accrued_cost, solution_path, start_vertex):
        predecessors = self.graph.get_predecessors(vertex)
        for predecessor in predecessors:
            key = (predecessor,vertex)
            weight = self.graph.get_weight(predecessor, vertex)
            if key in label and accrued_cost in label[key]:
                substraction = self._substract_lists(accrued_cost, weight)
                solution_path.add_edge(predecessor, vertex, weights=weight)

                if predecessor != start_vertex:
                    self._backtrack_sol(label, predecessor, substraction, solution_path, start_vertex)

                return





