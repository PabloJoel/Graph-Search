import heapq

import pandas as pd

from Algorithms.Algorithm import Algorithm
from Graphs.Graph import Graph
from Visualizers.ConsoleVisualizer import ConsoleVisualizer


class Heap:
    def __init__(self):
        self.vertex_label = dict()
        self.cost_vertex = dict()
        self.heap = list()
        heapq.heapify(self.heap)

    def contains_vertex(self, vertex):
        """
        Returns True if elem is in the Heap.
        :param elem:
        :return:
        """
        return vertex in self.vertex_label

    def pop(self):
        """
        Returns the minimun lexicographic element, by comparing cost1 and cost2.
        :return:
        """
        key = heapq.heappop(self.heap)
        vertex = self.cost_vertex[key][0]

        self.cost_vertex[key].remove(vertex)
        if len(self.cost_vertex[key]) == 0:
            del self.cost_vertex[key]

        value = self.vertex_label[vertex]
        del self.vertex_label[vertex]
        return value

    def push(self, elem):
        """
        Inserts an elem into the Heap.
        :param elem:
        :return:
        """
        key = (elem[1], elem[2])
        vertex = elem[0]

        if self.contains_vertex(vertex):
            raise ValueError(f"You cant push a vertex that is already in, you have to do a decrease-key instead. Label: {elem} is already inside.")

        heapq.heappush(self.heap, key)
        self.vertex_label[vertex] = elem
        if key in self.cost_vertex:
            self.cost_vertex[key].append(vertex)
        else:
            self.cost_vertex[key] = [vertex]

    def decrease_key(self, elem):
        """
        Decreases the cost of an already existing key.
        :param elem:
        :return:
        """
        vertex = elem[0]
        label_to_remove = self.vertex_label[vertex]

        new_cost, old_cost = (elem[1], elem[2]), (label_to_remove[1], label_to_remove[2])
        if self._check_dominance(new_cost, old_cost):
            raise ValueError(f"Error, new cost:{elem} is worse than old cost:{label_to_remove}. Decrease key should only improve the label.")

        self.remove(label_to_remove)
        self.push(elem)

    def _check_dominance(self, costs1, costs2):
        if len(costs1) != len(costs2):
            raise ValueError(
                f"Error, both costs must have the same size, but cost1:{costs1} and cost2:{costs2} have different sizes")

        as_good = True
        is_better = False

        c1, t1 = costs1[0], costs1[1]
        c2, t2 = costs2[0], costs2[1]
        if c2 > c1 or t2 > t1:
            as_good = False  # List2 is worse than List1

        if c2 < c1 or t2 < t1:
            is_better = True  # List2 is better than Cost1

        return as_good and is_better

    def remove(self, elem):
        """
        Removes a specific element from the Heap.
        :param elem:
        :return:
        """
        key = (elem[1], elem[2])
        vertex = elem[0]

        self.heap.remove(key)
        heapq.heapify(self.heap)

        del self.vertex_label[vertex]

        self.cost_vertex[key].remove(vertex)
        if len(self.cost_vertex[key]) == 0:
            del self.cost_vertex[key]

    def size(self):
        """
        Returns the number of elements inside the Heap
        :return:
        """
        return len(self.heap)


class BDijkstra(Algorithm):
    """
    MOA* algorithm
    """

    def __init__(self, graph: Graph, visualizer=ConsoleVisualizer()):
        """
        Creates the algorithm by using the input graph that contains the data, and by creating an empty Graph where the
        solution is going to be added later.
        The solution graph is created using the same parameters as the input graph, but empty.
        :param Graph graph: input graph containing the data.
        :param Visualizer visualizer: visualizer implementation to visualize the graphs. By default: ConsoleVisualizer.
        :param heuristic: heuristic function to be used. By default: BFS Heuristic.
        """

        super().__init__(graph, visualizer)

        # Specific Algorithm Parameters
        self.heap, self.d1, self.d2, self.L, self.start_vertex = None, None, None, None, None

    def step(self):
        """
        Run one step of the algorithm.
        :return:
        """
        pass

    def run(self, start_vertex, end_vertex, show_by_step=False, show_end=False):
        """
        Runs the algorithm from start_vertex until there are no more vertices to explore or end_vertex has been explored.
        :param str start_vertex:
        :param str or list end_vertices:
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

        if start_vertex in all_vertices and end_vertex in all_vertices and start_vertex != end_vertex:
            self.start_vertex = start_vertex
            self.heap = Heap()
            self.L = {vertex: list() for vertex in all_vertices}
            self.d1 = {vertex: float('inf') if vertex != start_vertex else 0 for vertex in all_vertices}
            self.d2 = {vertex: float('inf') if vertex != start_vertex else 0 for vertex in all_vertices}

            ls = (start_vertex, self.d1[start_vertex], self.d2[start_vertex], None)
            self.heap.push(ls)

            while self.heap.size() > 0:
                l_star = self.heap.pop()
                i = l_star[0]
                self.L[i].append(l_star)
                self.L[i] = self._get_nd_subset(self.L[i])

                lnew = self.new_candidate_label(i, l_star)
                if lnew is not None:
                    self.heap.push(lnew)
                    self.d1[i] = lnew[1]
                    self.d2[i] = lnew[2]
                self.relaxation_process(i, l_star)

            for sol in self.L[end_vertex]:
                solution_path = solution_template.copy()
                self._backtrack_sol(sol, solution_path)
                self.solution.add_solution(end_vertex, solution_path)

        if self.solution.is_empty():
            print(f'Warning, could not find a path from {start_vertex} to {end_vertex}')

        if show_end:
            self.visualizer.show(graph=self.graph)
            self.visualizer.show(graph=self.solution.get_all_solutions())

    def new_candidate_label(self, vertex, l_star):
        for predecessor in self.graph.get_predecessors(vertex):
            c1, c2 = self.graph.get_weight(predecessor, vertex)
            for l in self.L[predecessor]:
                check_label = (vertex, l[1] + c1, l[2] + c2, predecessor)
                if not self.is_dominated((check_label[1], check_label[2]), (l_star[1], l_star[2])) \
                        and check_label != l_star and check_label not in self.L[vertex]: # New label is not dominated by current label
                    return check_label

        return None

    def relaxation_process(self, vertex, l_star):
        for successor in self.graph.get_successors(vertex):
            c1, c2 = self.graph.get_weight(vertex, successor)
            new_cost = (l_star[1] + c1, l_star[2] + c2)
            if not self.is_dominated(new_cost, (self.d1[successor], self.d2[successor])):
                relaxation = len(self.L[successor]) == 0
                if not relaxation:
                    for label in self.L[successor]:
                        if (l_star[1] + c1) > label[1] and (l_star[2] + c2) < label[2]:
                            relaxation = True

                if relaxation:
                    # non dominated label
                    self.d1[successor] = l_star[1] + c1
                    self.d2[successor] = l_star[2] + c2
                    lnew = (successor, self.d1[successor], self.d2[successor], vertex)
                    if not self.heap.contains_vertex(lnew[0]):
                        self.heap.push(lnew)
                    else:
                        new_cost = (lnew[1], lnew[2])
                        label_to_replace = self.heap.vertex_label[lnew[0]]
                        if not self.is_dominated(new_cost, (label_to_replace[1], label_to_replace[2])):
                            self.heap.decrease_key(lnew)

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
        costs = [(elem[1], elem[2]) for elem in elements]
        subset = list()
        for elem in elements:
            if not self.is_dominated((elem[1], elem[2]), costs):
                subset.append(elem)
        return subset

    def _substract_costs(self, list1, list2):
        if len(list1) != len(list2):
            raise ValueError(f"Cant substract {list1} and {list2} as they have different sizes.")

        res = list()
        for c1, c2 in zip(list1, list2):
            res.append(c1-c2)
        return tuple(res)

    def _backtrack_sol(self, label, solution_path):
        vertex = label[0]
        my_cost = (label[1], label[2])
        predecessor = label[3]
        weight = self.graph.get_weight(predecessor, vertex)
        for elem in self.L[predecessor]:
            predecessor_cost = (elem[1], elem[2])
            if self._substract_costs(my_cost, weight) == predecessor_cost:
                solution_path.add_edge(predecessor, vertex, weights=weight)
                if predecessor != self.start_vertex:
                    self._backtrack_sol(elem, solution_path)
                return
