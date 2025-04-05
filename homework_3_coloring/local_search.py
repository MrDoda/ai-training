import numpy as np
import time
import math

# Attempt to import Numba's CUDA support.
try:
    from numba import cuda
    gpu_available = cuda.is_available()
except ImportError:
    gpu_available = False

def iscoloring(graph, colors):
    """
    Verify that the given coloring is valid.
    Returns True if no adjacent vertices share the same color.
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
    (This function is available for debugging or alternative approaches.)
    """
    conflicted = set()
    for u, v in graph.edges:
        if colors[u] == colors[v]:
            conflicted.add(u)
            conflicted.add(v)
    return list(conflicted)

def color(graph, k, steps, use_gpu=False, random_walk_prob=0.4, min_hill_climb=100):
    """
    Attempts to find a valid k-coloring of the graph using an incremental hill climbing approach.
    
    Instead of simulated annealing, this version forces hill climbing moves for at least
    `min_hill_climb` consecutive steps. In these steps it always selects the best candidate move 
    (i.e., the move with the lowest delta in conflicts) even if it does not improve the conflict count.
    After a streak of hill climbing moves, with probability `random_walk_prob` a random move is allowed,
    resetting the streak.
    
    Parameters:
      graph            - an instance of Graph.
      k                - number of colors to use.
      steps            - maximum number of local search steps.
      use_gpu          - if True, GPU conflict counting is used to periodically verify the incremental conflict count.
      random_walk_prob - probability for a random move after the hill climbing streak.
      min_hill_climb   - minimum number of consecutive hill climbing moves before considering a random move.
    
    Returns:
      A tuple (colors, success) where:
         - colors: an array of color assignments for each vertex.
         - success: True if a valid coloring (zero unique conflicts) was found.
    
    The algorithm precomputes neighbor lists and maintains S, the sum of conflict counts (each conflict counted twice),
    so that the number of unique conflicts is S // 2.
    """
    n = graph.num_vertices

    if use_gpu:
        print("GPU acceleration for conflict checking is enabled.")
    
    # Initialize with a random coloring.
    colors = np.random.randint(0, k, size=n).astype(np.int32)
    
    # Precompute neighbor lists.
    neighbors = [[] for _ in range(n)]
    for u, v in graph.edges:
        neighbors[u].append(v)
        neighbors[v].append(u)
    
    # Compute initial conflicts for each vertex and S = sum(conflicts).
    conflicts = np.zeros(n, dtype=np.int32)
    S = 0
    for v in range(n):
        cnt = 0
        for nb in neighbors[v]:
            if colors[v] == colors[nb]:
                cnt += 1
        conflicts[v] = cnt
        S += cnt  # Each conflict is counted twice overall.
    
    step = 0
    hill_climb_streak = 0
    start_time = time.time()
    
    while step < steps and (S // 2) > 0:
        # Pick a vertex that is in conflict.
        conflicted_vertices = [v for v in range(n) if conflicts[v] > 0]
        if not conflicted_vertices:
            break
        v = np.random.choice(conflicted_vertices)
        current_color = colors[v]
        
        # Decide on new color.
        if hill_climb_streak < min_hill_climb:
            # Forced hill climbing: choose the best candidate move from all possible moves.
            old_conflicts_v = conflicts[v]
            candidate_moves = []
            for candidate in range(k):
                if candidate == current_color:
                    continue
                new_conflicts = 0
                for nb in neighbors[v]:
                    if colors[nb] == candidate:
                        new_conflicts += 1
                delta = new_conflicts - old_conflicts_v
                candidate_moves.append((candidate, delta))
            candidate_moves.sort(key=lambda x: x[1])
            new_color = candidate_moves[0][0]
            hill_climb_streak += 1
        else:
            # After a sufficient hill climbing streak, with probability random_walk_prob, allow a random move.
            if np.random.rand() < random_walk_prob:
                new_color = np.random.randint(0, k)
                hill_climb_streak = 0
            else:
                old_conflicts_v = conflicts[v]
                candidate_moves = []
                for candidate in range(k):
                    if candidate == current_color:
                        continue
                    new_conflicts = 0
                    for nb in neighbors[v]:
                        if colors[nb] == candidate:
                            new_conflicts += 1
                    delta = new_conflicts - old_conflicts_v
                    candidate_moves.append((candidate, delta))
                candidate_moves.sort(key=lambda x: x[1])
                new_color = candidate_moves[0][0]
                hill_climb_streak += 1
        
        # Update the color and conflict counts if a change is made.
        if new_color != current_color:
            old_conflicts_v = conflicts[v]
            # Update neighbors' conflict counts and adjust S.
            for nb in neighbors[v]:
                if colors[nb] == current_color:
                    conflicts[nb] -= 1
                    S -= 1
                if colors[nb] == new_color:
                    conflicts[nb] += 1
                    S += 1
            # Update v's conflict count.
            new_conflict_v = 0
            for nb in neighbors[v]:
                if colors[nb] == new_color:
                    new_conflict_v += 1
            S = S - old_conflicts_v + new_conflict_v
            conflicts[v] = new_conflict_v
            colors[v] = new_color
        
        step += 1
        
        if use_gpu and step % 1000 == 0:
            gpu_conflicts = count_conflicts_gpu(graph, colors)
            if gpu_conflicts * 2 != S:
                print("Updating incremental conflict count S from GPU check.")
                S = gpu_conflicts * 2
        
        if step % 1000 == 0:
            elapsed = time.time() - start_time
            print(f"Step {step}, unique_conflicts: {S // 2}, hill_climb_streak: {hill_climb_streak}, elapsed: {elapsed:.2f}s")
    
    elapsed_total = time.time() - start_time
    print(f"Search finished in {elapsed_total:.2f} seconds with unique_conflicts: {S // 2}")
    return colors, ((S // 2) == 0)
