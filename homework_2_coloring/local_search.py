# local_search.py

import numpy as np
import time

# Attempt to import Numba's CUDA support.
try:
    from numba import cuda
    gpu_available = cuda.is_available()
except ImportError:
    gpu_available = False

def iscoloring(graph, colors):
    """
    Check if the given color assignment is a valid coloring for the graph.
    Returns True if no two adjacent vertices share the same color.
    """
    for u, v in graph.edges:
        if colors[u] == colors[v]:
            return False
    return True

def count_conflicts_cpu(graph, colors):
    """
    Count the total number of conflicting edges (where both endpoints share the same color)
    using a simple CPU loop.
    """
    conflicts = 0
    for u, v in graph.edges:
        if colors[u] == colors[v]:
            conflicts += 1
    return conflicts

if gpu_available:
    @cuda.jit
    def count_conflicts_kernel(edges, colors, conflict_array):
        i = cuda.grid(1)
        if i < edges.shape[0]:
            u = edges[i, 0]
            v = edges[i, 1]
            if colors[u] == colors[v]:
                conflict_array[i] = 1
            else:
                conflict_array[i] = 0

    def count_conflicts_gpu(graph, colors):
        """
        Count conflicts on the GPU.
        """
        m = graph.edges.shape[0]
        d_edges = cuda.to_device(graph.edges)
        d_colors = cuda.to_device(colors)
        conflict_arr = cuda.device_array(m, dtype=np.int32)
        threadsperblock = 256
        blockspergrid = (m + threadsperblock - 1) // threadsperblock
        count_conflicts_kernel[blockspergrid, threadsperblock](d_edges, d_colors, conflict_arr)
        conflicts = conflict_arr.copy_to_host()
        return int(np.sum(conflicts))
else:
    def count_conflicts_gpu(graph, colors):
        return count_conflicts_cpu(graph, colors)

def get_conflicted_vertices(graph, colors):
    """
    Returns a list of vertices that are incident to at least one conflicting edge.
    """
    conflicted = set()
    for u, v in graph.edges:
        if colors[u] == colors[v]:
            conflicted.add(u)
            conflicted.add(v)
    return list(conflicted)

def color(graph, k, steps, use_gpu=False, random_walk_prob=0.3):
    """
    Attempts to find a valid k-coloring of the graph using local search.
    
    Parameters:
      graph          - an instance of Graph.
      k              - number of colors to use.
      steps          - maximum number of local search steps.
      use_gpu        - if True, use GPU-accelerated conflict counting.
      random_walk_prob - probability of taking a random move (random walk) instead of hill climbing.
    
    Returns:
      A tuple (colors, success) where:
         - colors: an array of color assignments for each vertex.
         - success: a Boolean indicating whether a valid coloring was found.
    """
    n = graph.num_vertices
    # Initialize with a random coloring.
    colors = np.random.randint(0, k, size=n).astype(np.int32)
    conflict_func = count_conflicts_gpu if use_gpu else count_conflicts_cpu
    conflicts = conflict_func(graph, colors)
    step = 0
    start_time = time.time()

    while step < steps and conflicts > 0:
        conflicted_vertices = get_conflicted_vertices(graph, colors)
        if not conflicted_vertices:
            break
        # Choose a random vertex among those with conflicts.
        v = np.random.choice(conflicted_vertices)
        current_color = colors[v]
        # With a certain probability, perform a random move.
        if np.random.rand() < random_walk_prob:
            colors[v] = np.random.randint(0, k)
        else:
            # Otherwise, try all possible colors to minimize the number of conflicts.
            best_color = current_color
            best_conflicts = conflicts
            for new_color in range(k):
                if new_color == current_color:
                    continue
                temp_colors = colors.copy()
                temp_colors[v] = new_color
                new_conflicts = conflict_func(graph, temp_colors)
                if new_conflicts < best_conflicts:
                    best_conflicts = new_conflicts
                    best_color = new_color
            colors[v] = best_color
        conflicts = conflict_func(graph, colors)
        step += 1

        if step % 1000 == 0:
            elapsed = time.time() - start_time
            print(f"Step {step}, conflicts: {conflicts}, elapsed time: {elapsed:.2f}s")

    return colors, (conflicts == 0)
