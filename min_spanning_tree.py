import heapq
from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)  # adjacency list

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))  # Undirected graph

    def prim_mst(self):
        visited = [False] * self.V
        min_heap = [(0, 0)]  # (weight, vertex)
        mst_weight = 0
        mst_edges = []

        while min_heap:
            weight, u = heapq.heappop(min_heap)

            if visited[u]:
                continue

            visited[u] = True
            mst_weight += weight
            if weight != 0:
                mst_edges.append((prev_u, u, weight))

            for v, w in self.graph[u]:
                if not visited[v]:
                    heapq.heappush(min_heap, (w, v))
            prev_u = u

        print("Edges in MST:")
        for u, v, w in mst_edges:
            print(f"{u} - {v} : {w}")
        print(f"Total Weight of MST: {mst_weight}")

# Example Usage
g = Graph(5)
g.add_edge(0, 1, 2)
g.add_edge(0, 3, 6)
g.add_edge(1, 2, 3)
g.add_edge(1, 3, 8)
g.add_edge(1, 4, 5)
g.add_edge(2, 4, 7)
g.add_edge(3, 4, 9)

g.prim_mst()
