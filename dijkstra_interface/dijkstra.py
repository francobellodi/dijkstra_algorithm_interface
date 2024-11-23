# dijkstra.py

import heapq


class DijkstraAlgorithm:
    def __init__(self, graph, visualizer):
        self.graph = graph
        self.visualizer = visualizer
        self.queue = []
        self.distances = {}
        self.previous = {}
        self.visited = set()
        self.running = True
        self.paused = False
        self.counter = 0  # Initialize a counter for heap entries
        self.generator = None  # Will hold the generator object
        # Get the speed from the visualizer's speed slider
        self.speed = self.visualizer.speed_slider.get()
        self.state_stack = []  # Stack to keep track of states



    def run(self, start_node, end_node):
        self.generator = self.algorithm(start_node, end_node)
        # Start the algorithm without advancing it
        try:
            next(self.generator)
        except StopIteration:
            # The algorithm completed without needing steps
            self.visualizer.on_algorithm_complete(self.distances, self.previous)
            self.generator = None


    def algorithm(self, start_node, end_node):
        self.distances = {node: float('inf') for node in self.graph.nodes.values()}
        self.distances[start_node] = 0
        start_node.distance = 0
        self.visualizer.update_node_distance(start_node)
        queue = []
        self.counter += 1
        heapq.heappush(queue, (0, self.counter, start_node))

        while queue:
            current_distance, _, current_node = heapq.heappop(queue)

            if current_node in self.visited:
                continue

            # Save the state before processing
            state = {
                'queue': list(queue),
                'visited': set(self.visited),
                'distances': self.distances.copy(),
                'previous': self.previous.copy(),
                'current_node': current_node,
            }
            self.state_stack.append(state)

            self.visited.add(current_node)
            self.visualizer.highlight_node(current_node, 'yellow')

            # Move the car to current_node instantly
            self.visualizer.animate_car(None, None, current_node.x, current_node.y, animate=False)

            # Pause the algorithm until the user clicks "Next Step"
            yield  # Wait for user action

            if current_node == end_node:
                break

            for edge in current_node.edges:
                neighbor = edge.destination
                new_distance = self.distances[current_node] + edge.weight

                if new_distance < self.distances[neighbor]:
                    self.distances[neighbor] = new_distance
                    neighbor.distance = new_distance
                    self.previous[neighbor] = current_node

                    self.counter += 1
                    heapq.heappush(queue, (new_distance, self.counter, neighbor))

                    self.visualizer.highlight_edge(edge, 'blue')
                    self.visualizer.highlight_node(neighbor, 'orange')
                    self.visualizer.update_node_distance(neighbor)

                    # Animate the car moving to the neighbor node
                    self.visualizer.animate_car(current_node.x, current_node.y, neighbor.x, neighbor.y)

                    # Pause the algorithm until the animation is complete
                    yield  # Use yield instead of return

            self.visualizer.highlight_node(current_node, 'gray')

            # Pause after processing the current node
            yield

        # Algorithm has completed
        self.visualizer.on_algorithm_complete(self.distances, self.previous)

    def step_forward(self):
        if self.generator is None:
            return  # Algorithm has completed
        try:
            self.generator.send(None)
        except StopIteration:
            # Algorithm has completed
            self.visualizer.on_algorithm_complete(self.distances, self.previous)
            self.generator = None

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False
