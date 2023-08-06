import tkinter as tk
import heapq
from tkinter import messagebox
# FIRST INPUT - NAME OF THE NODE
# SECOND AND THIRD INPUT - ARE THE COORDINATES OF THE NODE
# THIRD INPUT IS THE WEIGHT OF THE EDGE

# FOR ADDING EDGE WITH THE WEIGHT - EX: A B AND IN THE THIRD INPUT PUT THE WEIGHT AND PRESS ADD WEIGHT IF WEIGHT IS NOT FILLED THE DEFAULT WEIGHT IS 1

class Graph:
    def __init__(self):
        self.graph = {}
        self.node_positions = {}  # Dictionary to store node positions

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_node_position(self, node, x, y):
        self.add_node(node)
        self.node_positions[node] = (x, y)  # Store node position

    def add_edge(self, u, v, weight=1):
        self.add_node(u)
        self.add_node(v)
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=" ")

        for neighbor, _ in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

    def bfs(self, start):
        visited = set()
        queue = [start]
        visited.add(start)

        while queue:
            node = queue.pop(0)
            print(node, end=" ")

            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph.get(current_node, []):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

class GraphVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Visualizer")
        self.geometry("800x600")

        self.graph = Graph()

        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Canvas takes most of the space on the left

        input_frame = tk.Frame(self)
        input_frame.pack(side=tk.RIGHT, fill=tk.Y)  # Input frame takes space on the right

        self.node_entry = tk.Entry(input_frame)
        self.node_entry.pack()

        self.x_entry = tk.Entry(input_frame)
        self.x_entry.pack()

        self.y_entry = tk.Entry(input_frame)
        self.y_entry.pack()

        self.add_node_button = tk.Button(input_frame, text="Add Node", command=self.add_node)
        self.add_node_button.pack(fill=tk.X)

        self.add_edge_button = tk.Button(input_frame, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack(fill=tk.X)

        self.distance_button = tk.Button(input_frame, text="Find Distance", command=self.find_distance)
        self.distance_button.pack(fill=tk.X)

        self.weight_entry = tk.Entry(input_frame)  # New entry field for edge weight
        self.weight_entry.pack()

        # Add x and y axes
        self.canvas.create_line(0, 0, 800, 0, fill="black", width=2)
        self.canvas.create_line(0, 0, 0, 600, fill="black", width=2)
        self.canvas.create_text(400, 10, text="x", anchor="e")
        self.canvas.create_text(10, 300, text="y", anchor="n")

        

    def add_node(self):
        node = self.node_entry.get()
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())

        # Check for overlapping nodes
        while self.is_overlapping_node(x, y):
            x += 30
            y += 30

        self.graph.add_node_position(node, x, y)
        self.canvas.create_oval(x, y, x + 20, y + 20, fill="blue")  # Visualize nodes as blue ovals

    def add_edge(self):
        edge_input = self.node_entry.get().split()
        if len(edge_input) == 2:
            u, v = edge_input
            weight = 1  # Default weight is 1 if not provided

            # Check if the weight is provided and is a valid integer
            weight_input = self.weight_entry.get()
            if weight_input:
                try:
                    weight = int(weight_input)
                except ValueError:
                    messagebox.showerror("Error", "Invalid weight value. Please enter a valid integer.")
                    return

            self.graph.add_edge(u, v, weight)
            x1, y1 = self.graph.node_positions[u]
            x2, y2 = self.graph.node_positions[v]
            self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black", width=2)
        else:
            messagebox.showerror("Error", "Invalid input. Please enter the two nodes separated by spaces.")

    def find_distance(self):
        node1, node2 = self.node_entry.get().split()
        distances = self.graph.dijkstra(node1)
        distance = distances.get(node2, None)

        if distance is not None:
            messagebox.showinfo("Distance", f"The shortest distance between {node1} and {node2} is {distance}.")
        else:
            messagebox.showinfo("Distance", f"There is no path between {node1} and {node2}.")

    def is_overlapping_node(self, x, y):
        for node, (nx, ny) in self.graph.node_positions.items():
            if abs(x - nx) < 30 and abs(y - ny) < 30:
                return True
        return False

if __name__ == "__main__":
    app = GraphVisualizerApp()
    app.mainloop()
