# graph.py

import numpy as np

class Graph:
    def __init__(self, num_vertices, edges):
        self.num_vertices = num_vertices  # Number of vertices.
        self.edges = edges                # NumPy array of shape (m, 2) with 0-indexed vertices.

def load_graph(filename):
    """
    Load a graph from a .col file.
    The file should have lines like:
      c ...          (comments)
      p edge <num_vertices> <num_edges>
      e <vertex1> <vertex2>
    (Note: vertices in the file are assumed 1-indexed.)
    """
    num_vertices = 0
    edge_list = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('c'):
                continue
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 'p':
                # Example: p edge 125 1053
                num_vertices = int(parts[2])
            elif parts[0] == 'e':
                u = int(parts[1]) - 1  # convert to 0-indexed
                v = int(parts[2]) - 1
                edge_list.append((u, v))
    edges = np.array(edge_list, dtype=np.int32)
    return Graph(num_vertices, edges)
