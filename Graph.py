import heapq
import tkinter as tk

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

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

if __name__ == "__main__":
    g = Graph()
    g.add_edge('A', 'B', 5)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'D', 2)
    g.add_edge('C', 'D', 7)
    g.add_edge('D', 'E', 4)

    print("DFS Traversal:")
    g.dfs('A')

    print("\n\nBFS Traversal:")
    g.bfs('A')

    print("\n\nShortest Distances from Node 'A' using Dijkstra's Algorithm:")
    distances = g.dijkstra('A')
    print(distances)
