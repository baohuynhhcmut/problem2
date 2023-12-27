from collections import deque
from queue import PriorityQueue
from typing import List, Tuple

class SuccessiveShortestPathFlowNetwork:
    class Arc:
        def __init__(self, start: int, end: int, flow: int, capacity: int, cost: int):
            self.start_ = start
            self.end_ = end
            self.flow_ = flow
            self.capacity_ = capacity
            self.cost_ = cost

        def get_dest(self, from_: int) -> int:
            return self.end_ if from_ == self.start_ else self.start_

        def add_flow(self, from_: int, to_add: int) -> None:
            self.flow_ += to_add if from_ == self.start_ else -to_add

        def get_capacity(self, from_: int) -> int:
            return self.capacity_ - self.flow_ if from_ == self.start_ else self.flow_

        def get_cost_from(self, from_: int) -> int:
            return self.cost_ if from_ == self.start_ else -self.cost_

    class Node:
        def __init__(self, index: int):
            self.index_ = index
            self.connected_arcs_ = []

    def __init__(self):
        self.nodes_ = []
        self.arcs_ = deque()

    def add_node(self) -> None:
        self.nodes_.append(self.Node(len(self.nodes_)))

    def add_arc(self, start: int, end: int, flow: int, capacity: int, cost: int) -> int:
        self.arcs_.append(self.Arc(start, end, flow, capacity, cost))
        self.nodes_[start].connected_arcs_.append(self.arcs_[-1])
        self.nodes_[end].connected_arcs_.append(self.arcs_[-1])
        return len(self.arcs_) - 1

    def min_cost_max_flow(self, source_i: int, sink_i: int) -> int:
        result = 0
        potentials = [float('inf')] * len(self.nodes_)

        front = deque([(0, source_i)])
        while front:
            potential, cur_i = front.popleft()
            if potential >= potentials[cur_i]:
                continue
            potentials[cur_i] = potential

            for arc in self.nodes_[cur_i].connected_arcs_:
                if arc.get_capacity(cur_i) > 0:
                    front.append((potential + arc.get_cost_from(cur_i), arc.get_dest(cur_i)))
        while True:
            frontier = PriorityQueue()
            explr = [False] * len(self.nodes_)
            cost_to_node = [-1] * len(self.nodes_)
            arc_used = [None] * len(self.nodes_)
            frontier.put((0, source_i, None))

            while not frontier.empty():
                path_cost, cur_i, cur_arc_used = frontier.get()
                path_cost = -path_cost

                if not explr[cur_i]:
                    explr[cur_i] = True
                    arc_used[cur_i] = cur_arc_used
                    cost_to_node[cur_i] = path_cost

                    for arc in self.nodes_[cur_i].connected_arcs_:
                        if arc.get_capacity(cur_i) > 0:
                            next_i = arc.get_dest(cur_i)
                            frontier.put((-path_cost - (arc.get_cost_from(cur_i) - potentials[next_i] + potentials[cur_i]), next_i, arc))

            if arc_used[sink_i] is None:
                return result

            arcs = []
            flow_pushed = float('inf')
            cur_i = sink_i
            while cur_i != source_i:
                arc = arc_used[cur_i]
                cur_i = arc.get_dest(cur_i)
                flow_pushed = min(flow_pushed, arc.get_capacity(cur_i))
                arcs.append(arc)

            for arc in reversed(arcs):
                arc.add_flow(cur_i, flow_pushed)
                result += arc.get_cost_from(cur_i) * flow_pushed
                cur_i = arc.get_dest(cur_i)

            for i in range(len(self.nodes_)):
                if cost_to_node[i] != -1:
                    potentials[i] += cost_to_node[i]
        return result
        