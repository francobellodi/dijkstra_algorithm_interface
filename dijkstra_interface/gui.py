# gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from graph import Node, Edge, Graph
from dijkstra import DijkstraAlgorithm
from tkinter import Scale, HORIZONTAL
from PIL import Image, ImageTk
import math


class DijkstraVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Dijkstra's Algorithm Visualization")
        self.graph = Graph()
        self.create_widgets()
        self.bind_canvas_actions()
        self.dijkstra_thread = None
        self.algorithm = None
        # Load the car image
        self.car_image = Image.open("car.png")
        self.car_image = self.car_image.resize((30, 30), Image.LANCZOS)
        self.car_photo = ImageTk.PhotoImage(self.car_image)
        self.car_sprite = None  # Will be used to display the car on the canvas

    def animate_car(self, start_x, start_y, end_x, end_y, animate=True):
        if not animate:
            # Instant move
            if self.car_sprite:
                self.canvas.coords(self.car_sprite, end_x, end_y)
            else:
                self.car_sprite = self.canvas.create_image(end_x, end_y, image=self.car_photo)
            # Do not proceed automatically; wait for user input
        else:
            # Animated movement
            duration = 1000  # Duration in milliseconds
            steps = int(duration / 20)  # Number of steps in the animation
            delta_x = (end_x - start_x) / steps
            delta_y = (end_y - start_y) / steps
            self.animation_step = 0
            self.animation_steps = steps
            self.animation_delta_x = delta_x
            self.animation_delta_y = delta_y
            self.animation_start_x = start_x
            self.animation_start_y = start_y
            self.animation_end_callback = self.resume_algorithm  # Callback after animation

            # Disable the Next Step button during animation
            self.next_step_button.config(state=tk.DISABLED)

            # Start the animation
            self.move_car()

    def move_car(self):
        if self.animation_step <= self.animation_steps:
            x = self.animation_start_x + self.animation_delta_x * self.animation_step
            y = self.animation_start_y + self.animation_delta_y * self.animation_step
            if self.car_sprite:
                self.canvas.coords(self.car_sprite, x, y)
            else:
                self.car_sprite = self.canvas.create_image(x, y, image=self.car_photo)
            self.animation_step += 1
            self.root.after(20, self.move_car)
        else:
            # Animation complete
            if self.animation_end_callback:
                self.animation_end_callback()

    def resume_algorithm(self):
        # Re-enable the Next Step button
        self.next_step_button.config(state=tk.NORMAL)
        # Proceed to the next step automatically
        if self.algorithm:
            self.algorithm.step_forward()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack(side=tk.LEFT)

        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Speed control slider
        speed_label = tk.Label(control_frame, text="Algorithm Speed")
        speed_label.pack(pady=5)
        self.speed_slider = Scale(control_frame, from_=0.1, to=2.0, orient=HORIZONTAL, resolution=0.1)
        self.speed_slider.set(1.0)  # Default speed
        self.speed_slider.pack(pady=5)

        self.mode_label = tk.Label(control_frame, text="Current Mode: None")
        self.mode_label.pack(pady=5)

        self.add_node_button = tk.Button(control_frame, text="Add Node", command=self.add_node_mode)
        self.add_node_button.pack(pady=5)

        self.set_start_button = tk.Button(control_frame, text="Set Start Node", command=self.set_start_mode)
        self.set_start_button.pack(pady=5)

        self.set_end_button = tk.Button(control_frame, text="Set End Node", command=self.set_end_mode)
        self.set_end_button.pack(pady=5)

        self.draw_edge_button = tk.Button(control_frame, text="Draw Edge", command=self.draw_edge_mode)
        self.draw_edge_button.pack(pady=5)

        self.edit_edge_button = tk.Button(control_frame, text="Edit Edge", command=self.edit_edge_mode)
        self.edit_edge_button.pack(pady=5)

        self.run_button = tk.Button(control_frame, text="Run Dijkstra's Algorithm", command=self.run_dijkstra)
        self.run_button.pack(pady=5)

        self.reset_button = tk.Button(control_frame, text="Reset Graph", command=self.reset_graph)
        self.reset_button.pack(pady=5)

        self.status_label = tk.Label(control_frame, text="")
        self.status_label.pack(pady=20)

        # Add the Clear Response button
        self.clear_response_button = tk.Button(
            control_frame, text="Clear Response", command=self.clear_response
        )
        self.clear_response_button.pack(pady=5)
        self.clear_response_button.config(state=tk.DISABLED)  # Initially disabled

        self.status_label = tk.Label(control_frame, text="")
        self.status_label.pack(pady=20)

        self.next_step_button = tk.Button(control_frame, text="Next Step", command=self.next_step)
        self.next_step_button.pack(pady=5)

        # Disable buttons until the algorithm is run
        self.next_step_button.config(state=tk.DISABLED)

    def bind_canvas_actions(self):
        self.canvas.bind("<Button-1>", self.canvas_click)

    def clear_response(self):
        # Reset node colors and distances
        for node in self.graph.nodes.values():
            node.distance = float('inf')  # Reset distance to infinity
            node.visited = False  # Reset visited status if used
            self.update_node_color(node)
            self.update_node_distance(node)

        # Reset edge colors
        for edge in self.graph.edges:
            self.canvas.itemconfig(edge.graphics[0], fill='black')  # Default edge color

        # Clear algorithm-specific data
        if self.algorithm:
            self.algorithm.visited.clear()
            self.algorithm.distances.clear()
            self.algorithm.previous.clear()
            self.algorithm.running = False  # Ensure the algorithm is stopped

        # Disable the Clear Response button again
        self.clear_response_button.config(state=tk.DISABLED)

        # Update the status label or any other UI elements
        self.status_label.config(text="Graph reset to initial state.")


    def canvas_click(self, event):
        if self.current_mode == 'add_node':
            self.create_node(event)
        elif self.current_mode == 'set_start':
            self.select_start_node(event)
        elif self.current_mode == 'set_end':
            self.select_end_node(event)
        elif self.current_mode == 'draw_edge':
            self.select_edge_nodes(event)
        elif self.current_mode == 'edit_edge':
            self.select_edge_to_edit(event)

    def add_node_mode(self):
        self.current_mode = 'add_node'
        self.mode_label.config(text="Current Mode: Add Node")
        self.clear_selected_nodes()

    def create_node(self, event):
        x, y = event.x, event.y
        node_id = len(self.graph.nodes)
        node = Node(node_id, x, y)
        self.graph.add_node(node)
        self.draw_node(node)

    def draw_node(self, node):
        color = 'blue'
        if node.node_type == 'start':
            color = 'green'
            node.distance = 0
        elif node.node_type == 'end':
            color = 'red'
        node_shape = self.canvas.create_oval(
            node.x - 15, node.y - 15, node.x + 15, node.y + 15, fill=color
        )
        node_label = self.canvas.create_text(node.x, node.y, text=str(node.id))

        # Changes to the distance label
        distance_label = self.canvas.create_text(
            node.x, node.y + 25, text=self.format_distance(node.distance),
            fill='red', font=('Arial', 12, 'bold')
        )
        node.graphics = (node_shape, node_label, distance_label)

    def update_node_distance(self, node):
        self.canvas.itemconfig(
            node.graphics[2],
            text=self.format_distance(node.distance),
            fill='red',
            font=('Arial', 12, 'bold')
        )

    def format_distance(self, distance):
        return "∞" if distance == float('inf') else str(distance)

    def set_start_mode(self):
        self.current_mode = 'set_start'
        self.mode_label.config(text="Current Mode: Set Start Node")
        self.clear_selected_nodes()

    def select_start_node(self, event):
        node = self.graph.get_node_at(event.x, event.y)
        if node:
            self.graph.set_start_node(node)
            self.update_node_color(node)
            self.mode_label.config(text="Current Mode: None")
            self.current_mode = None

    def set_end_mode(self):
        self.current_mode = 'set_end'
        self.mode_label.config(text="Current Mode: Set End Node")
        self.clear_selected_nodes()

    def select_end_node(self, event):
        node = self.graph.get_node_at(event.x, event.y)
        if node:
            self.graph.set_end_node(node)
            self.update_node_color(node)
            self.mode_label.config(text="Current Mode: None")
            self.current_mode = None

    def update_node_color(self, node):
        color = 'blue'
        if node.node_type == 'start':
            color = 'green'
        elif node.node_type == 'end':
            color = 'red'
        self.canvas.itemconfig(node.graphics[0], fill=color)
        self.update_node_distance(node)

    def draw_edge_mode(self):
        self.current_mode = 'draw_edge'
        self.mode_label.config(text="Current Mode: Draw Edge")
        self.selected_nodes = []

    def select_edge_nodes(self, event):
        node = self.graph.get_node_at(event.x, event.y)
        if node and node not in self.selected_nodes:
            self.selected_nodes.append(node)
            self.highlight_node(node, 'yellow')
            if len(self.selected_nodes) == 1:
                self.mode_label.config(text="Selected first node. Select second node.")
            elif len(self.selected_nodes) == 2:
                self.mode_label.config(text="Selected second node. Drawing edge...")
                self.prompt_edge_weight()
                self.mode_label.config(text="Current Mode: Draw Edge")

    def prompt_edge_weight(self):
        weight = simpledialog.askfloat("Edge Weight", "Enter the weight for the edge:", minvalue=0.0)
        if weight is None:
            weight = 1.0
        direction = messagebox.askyesno("Edge Direction", "Is the edge directed?")
        edge = Edge(self.selected_nodes[0], self.selected_nodes[1], weight, directed=direction)
        self.graph.add_edge(edge)
        self.draw_edge(edge)
        self.clear_selected_nodes()
        # Comment out or remove the following lines
        # self.mode_label.config(text="Current Mode: None")
        # self.current_mode = None

    def draw_edge(self, edge):
        x1, y1 = edge.source.x, edge.source.y
        x2, y2 = edge.destination.x, edge.destination.y
        line = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST if edge.directed else tk.NONE)
        weight_label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(edge.weight))
        edge.graphics = (line, weight_label)

    def clear_selected_nodes(self):
        for node in self.selected_nodes:
            self.highlight_node(node, 'blue' if node.node_type == 'intermediate' else 'green' if node.node_type == 'start' else 'red')
        self.selected_nodes = []

    def highlight_node(self, node, color):
        self.canvas.itemconfig(node.graphics[0], fill=color)
        self.update_node_distance(node)

    def highlight_edge(self, edge, color):
        self.canvas.itemconfig(edge.graphics[0], fill=color)

    def edit_edge_mode(self):
        self.current_mode = 'edit_edge'
        self.mode_label.config(text="Current Mode: Edit Edge")
        self.clear_selected_nodes()

    def select_edge_to_edit(self, event):
        edge = self.get_edge_at(event.x, event.y)
        if edge:
            # Highlight the edge to indicate selection
            self.highlight_edge(edge, 'yellow')
            self.prompt_edit_edge(edge)
            # After editing, reset the edge color
            self.highlight_edge(edge, 'black')
            self.mode_label.config(text="Current Mode: None")
            self.current_mode = None
        else:
            messagebox.showinfo("Info", "No edge found at this location.")

    def prompt_edit_edge(self, edge):
        weight = simpledialog.askfloat("Edge Weight", "Enter the new weight for the edge:", initialvalue=edge.weight, minvalue=0.0)
        if weight is not None:
            edge.weight = weight
            self.canvas.itemconfig(edge.graphics[1], text=str(edge.weight))
        direction = messagebox.askyesno("Edge Direction", "Is the edge directed?")
        edge.directed = direction
        self.canvas.itemconfig(edge.graphics[0], arrow=tk.LAST if edge.directed else tk.NONE)

    def get_edge_at(self, x, y):
        tolerance = 5  # Adjust this value as needed
        for edge in self.graph.edges:
            x1, y1 = edge.source.x, edge.source.y
            x2, y2 = edge.destination.x, edge.destination.y
            # Compute the distance from the point to the edge
            distance = self.point_to_segment_distance(x, y, x1, y1, x2, y2)
            if distance <= tolerance:
                return edge
        return None

    def point_to_segment_distance(self, px, py, x1, y1, x2, y2):
        # Compute the distance from point (px, py) to the segment (x1, y1)-(x2, y2)
        line_mag = math.hypot(x2 - x1, y2 - y1)
        if line_mag < 1e-8:
            return math.hypot(px - x1, py - y1)

        u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
        if u < 0 or u > 1:
            # Closest point does not fall within the segment
            dist1 = math.hypot(px - x1, py - y1)
            dist2 = math.hypot(px - x2, py - y2)
            return min(dist1, dist2)
        else:
            # Intersecting point is within the segment
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            return math.hypot(px - ix, py - iy)

    def run_dijkstra(self):
        start_node = self.graph.get_start_node()
        end_node = self.graph.get_end_node()
        if not start_node or not end_node:
            messagebox.showerror("Error", "Start or end node not defined.")
            return
        self.clear_response_button.config(state=tk.DISABLED)  # Disable before running
        self.algorithm = DijkstraAlgorithm(self.graph, self)
        self.algorithm.speed = self.speed_slider.get()  # Get current speed
        self.algorithm.run(start_node, end_node)
        # Enable the Clear Response button after the algorithm finishes
        # Enable step buttons
        self.next_step_button.config(state=tk.NORMAL)
        self.clear_response_button.config(state=tk.NORMAL)


    def next_step(self):
        if self.algorithm:
            self.algorithm.step_forward()


    def highlight_shortest_path(self, previous, start_node, end_node):
        node = end_node
        while node != start_node:
            prev_node = previous[node]
            edge = self.find_edge(prev_node, node)
            if edge:
                self.highlight_edge(edge, 'green')
            self.highlight_node(node, 'green')
            node = prev_node
        self.highlight_node(start_node, 'green')

    def find_edge(self, source, destination):
        for edge in self.graph.edges:
            if edge.source == source and edge.destination == destination:
                return edge
        return None

    def display_total_distance(self, distance):
        messagebox.showinfo("Shortest Path", f"The total distance is {distance}")
        # Enable the Clear Response button
        self.clear_response_button.config(state=tk.NORMAL)

    def show_no_path_message(self):
        messagebox.showinfo("No Path", "No path exists between the start and end nodes.")
        # Enable the Clear Response button
        self.clear_response_button.config(state=tk.NORMAL)

    def reset_graph(self):
        self.canvas.delete("all")
        self.graph = Graph()
        self.current_mode = None
        self.mode_label.config(text="Current Mode: None")

    def update(self):
        self.root.update()

    def on_algorithm_complete(self, distances, previous):
        self.highlight_shortest_path(previous, self.graph.get_start_node(), self.graph.get_end_node())
        total_distance = distances[self.graph.get_end_node()]
        self.display_total_distance(total_distance)

        # Remove the car sprite
        if self.car_sprite:
            self.canvas.delete(self.car_sprite)
            self.car_sprite = None  # Ensure this line is present

        # Disable step buttons
        self.next_step_button.config(state=tk.DISABLED)

    def restore_state(self, distances, previous, visited, current_node, car_position):
        # Reset the visualization
        for node in self.graph.nodes.values():
            color = 'blue'
            if node.node_type == 'start':
                color = 'green'
            elif node.node_type == 'end':
                color = 'red'
            elif node in visited:
                color = 'gray'
            self.canvas.itemconfig(node.graphics[0], fill=color)
            node.distance = distances[node]
            self.update_node_distance(node)

        # Reset edge colors
        for edge in self.graph.edges:
            self.canvas.itemconfig(edge.graphics[0], fill='black')

        # Highlight current node
        if current_node:
            self.canvas.itemconfig(current_node.graphics[0], fill='yellow')

        # Highlight edges in previous
        for node, prev_node in previous.items():
            edge = self.find_edge(prev_node, node)
            if edge:
                self.highlight_edge(edge, 'blue')

        # Restore the car's position
        if car_position:
            self.animate_car(*car_position)
        else:
            if self.car_sprite:
                self.canvas.delete(self.car_sprite)
                self.car_sprite = None  # Ensure this line is present

        self.root.update()

