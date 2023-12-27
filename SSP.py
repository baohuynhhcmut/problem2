# mincost-flow problem
import heapq
from typing import List, Tuple
class SuccessiveShortestPathFlowNetwork:
    class Arc:
        def __init__(self, start, end, flow, capacity, cost):
            self.start = start
            self.end = end
            self.flow = flow
            self.capacity = capacity
            self.cost = cost
        
        def get_dest(self, from_node):
            return self.end if from_node == self.start else self.start
        
        def add_flow(self, from_node, to_add):
            if from_node == self.start:
                self.flow += to_add
            else:
                self.flow -= to_add
        
        def get_capacity(self, from_node):
            return self.capacity - self.flow if from_node == self.start else self.flow
        
        def get_cost_from(self, from_node):
            return self.cost if from_node == self.start else -self.cost

    class Node:
        def __init__(self, index):
            self.index = index
            self.connected_arcs = []

    def __init__(self):
        self.nodes = []
        self.arcs = []

    def add_node(self):
        self.nodes.append(self.Node(len(self.nodes)))
    
    def add_arc(self, start, end, flow, capacity, cost):
        arc = self.Arc(start, end, flow, capacity, cost)
        self.arcs.append(arc)
        self.nodes[start].connected_arcs.append(arc)
        self.nodes[end].connected_arcs.append(arc)
        return len(self.arcs) - 1

    def min_cost_max_flow(self, source_i, sink_i):
        result = 0
        
        potentials = [float('inf')] * len(self.nodes)
        front = [(0, source_i)]
        
        while front:
            potential, cur_i = front.pop(0)
            
            if potential >= potentials[cur_i]:
                continue
            
            potentials[cur_i] = potential
            
            for arc in self.nodes[cur_i].connected_arcs:
                if arc.get_capacity(cur_i) > 0:
                    front.append((potential + arc.get_cost_from(cur_i), arc.get_dest(cur_i)))
            
        while True:
            frontier = [(-0, source_i, None)]
            explr = [False] * len(self.nodes)
            cost_to_node = [-1] * len(self.nodes)
            arc_used = [None] * len(self.nodes)
            
            heapq.heapify(frontier)
            
            while frontier:
                path_cost, cur_i, cur_arc_used = heapq.heappop(frontier)
                path_cost = -path_cost
                
                if not explr[cur_i]:
                    explr[cur_i] = True
                    arc_used[cur_i] = cur_arc_used
                    cost_to_node[cur_i] = path_cost
                    
                    for arc in self.nodes[cur_i].connected_arcs:
                        if arc.get_capacity(cur_i) > 0:
                            next_i = arc.get_dest(cur_i)
                            heapq.heappush(frontier, (
                                -(path_cost + (arc.get_cost_from(cur_i) - potentials[next_i] + potentials[cur_i])),
                                next_i,
                                arc
                            ))
            
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
            
            for i in range(len(self.nodes)):
                if cost_to_node[i] != -1:
                    potentials[i] += cost_to_node[i]

    
        






