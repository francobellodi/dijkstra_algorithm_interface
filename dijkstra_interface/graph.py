# graph.py
import math  # Add this import for infinity

class Node:
    def __init__(self, node_id, x, y, node_type='intermediate'):
        self.id = node_id
        self.x = x
        self.y = y
        self.edges = []
        self.node_type = node_type  # 'start', 'end', or 'intermediate'
        self.distance = math.inf  # Initialize distance to infinity

    def add_edge(self, edge):
        self.edges.append(edge)

class Edge:
    def __init__(self, source, destination, weight, directed=False):
        self.source = source
        self.destination = destination
        self.weight = weight
        self.directed = directed

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.start_node = None
        self.end_node = None

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, edge):
        self.edges.append(edge)
        edge.source.add_edge(edge)
        if not edge.directed:
            reverse_edge = Edge(edge.destination, edge.source, edge.weight, directed=False)
            self.edges.append(reverse_edge)
            edge.destination.add_edge(reverse_edge)

    def get_node_at(self, x, y):
        for node in self.nodes.values():
            if (node.x - x) ** 2 + (node.y - y) ** 2 <= 400:  # within 20 pixels radius
                return node
        return None

    def set_start_node(self, node):
        if self.start_node:
            self.start_node.node_type = 'intermediate'
        self.start_node = node
        node.node_type = 'start'

    def set_end_node(self, node):
        if self.end_node:
            self.end_node.node_type = 'intermediate'
        self.end_node = node
        node.node_type = 'end'

    def get_start_node(self):
        return self.start_node

    def get_end_node(self):
        return self.end_node
