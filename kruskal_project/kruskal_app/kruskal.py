import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Django
import networkx as nx
import matplotlib.pyplot as plt
import os
import heapq

# Disjoint Set for Kruskal's Algorithm
class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])  # Path compression
        return self.parent[v]

    def union(self, v1, v2):
        root1 = self.find(v1)
        root2 = self.find(v2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

# Kruskal's Algorithm
def kruskal(vertices, edges):
    if not vertices or not edges:
        return []
    
    edges.sort(key=lambda edge: edge[2])  # Sort edges by weight
    ds = DisjointSet(vertices)
    mst = []
    priority = 1

    for v1, v2, weight in edges:
        if ds.find(v1) != ds.find(v2):
            mst.append((v1, v2, weight, priority))
            ds.union(v1, v2)
            priority += 1
    
    return mst

# Prim's Algorithm
def prim(vertices, edges, start_vertex):
    if not vertices or not edges or start_vertex not in vertices:
        return []

    mst = []
    visited = set()
    min_heap = []
    
    visited.add(start_vertex)
    priority = 1
    
    for v1, v2, weight in edges:
        if v1 == start_vertex or v2 == start_vertex:
            heapq.heappush(min_heap, (weight, v1, v2))

    while len(mst) < len(vertices) - 1 and min_heap:
        weight, v1, v2 = heapq.heappop(min_heap)
        if v1 in visited and v2 in visited:
            continue

        mst.append((v1, v2, weight, priority))
        priority += 1
        new_vertex = v2 if v1 in visited else v1
        visited.add(new_vertex)

        for edge in edges:
            v1, v2, weight = edge
            if (v1 == new_vertex and v2 not in visited) or (v2 == new_vertex and v1 not in visited):
                heapq.heappush(min_heap, (weight, v1, v2))
    
    return mst

def visualize_graph(vertices, edges, mst, image_path):
    if not vertices or not edges:
        return

    G = nx.Graph()
    for v1, v2, weight in edges:
        G.add_edge(v1, v2, weight=weight)

    # 🔹 Use a fixed seed to maintain the same layout
    pos = nx.spring_layout(G, seed=42)  

    plt.figure(figsize=(8, 6))

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1500, font_size=12)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight MST edges in red
    if mst:
        mst_edges = [(v1, v2) for v1, v2, _, _ in mst]
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=2.5, edge_color='red')

    plt.title("Graph Visualization")
    plt.savefig(image_path)
    plt.close()


# Function to Check Graph Connectivity
def is_graph_connected(vertices, edges):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from([(v1, v2) for v1, v2, _ in edges])

    return nx.is_connected(G)
