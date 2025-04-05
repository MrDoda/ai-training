import argparse
import time
import json
from datetime import datetime
from graph import load_graph
from local_search import color, iscoloring, count_conflicts_cpu, count_conflicts_gpu
from visualize_graph import visualize_coloring
from interactive_html_report import update_html_report
from card_generator import generate_card_html

def generate_graph_json(graph, colors):
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
               "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
               "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
               "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"]
    nodes = []
    for i in range(graph.num_vertices):
        col = palette[colors[i] % len(palette)]
        nodes.append({"data": {"id": str(i), "label": str(i), "color": col}})
    edges = []
    for idx, (u, v) in enumerate(graph.edges):
        edges.append({"data": {"id": f"e{idx}", "source": str(u), "target": str(v)}})
    return json.dumps({"nodes": nodes, "edges": edges})

def main():
    parser = argparse.ArgumentParser(
        description="Graph Coloring via local search with interactive graph preview."
    )
    parser.add_argument("file", help="Path to .col graph file (e.g., dsjc125.9.col)")
    parser.add_argument("--colors", type=int, default=44, help="Number of colors to use (default: 44)")
    parser.add_argument("--steps", type=int, default=100000, help="Maximum number of local search steps")
    parser.add_argument("--random", type=float, default=0.3, help="Probability for random walk moves (default: 0.3)")
    parser.add_argument("--min_hill_climb", type=int, default=100, help="Minimum number of consecutive hill climbing moves (default: 100)")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU acceleration for conflict counting")
    args = parser.parse_args()

    graph = load_graph(args.file)
    print(f"Graph loaded: {graph.num_vertices} vertices, {graph.edges.shape[0]} edges")

    if args.gpu:
        try:
            from numba import cuda
            if cuda.is_available():
                print("GPU acceleration enabled.")
            else:
                print("GPU acceleration requested but CUDA support is not available. Using CPU.")
        except ImportError:
            print("Numba CUDA not installed. Using CPU.")

    start_time = time.time()
    coloring, success = color(
        graph, args.colors, args.steps,
        use_gpu=args.gpu,
        random_walk_prob=args.random,
        min_hill_climb=args.min_hill_climb
    )
    elapsed_time = time.time() - start_time

    conflict_func = count_conflicts_gpu if args.gpu else count_conflicts_cpu
    final_conflicts = conflict_func(graph, coloring)

    print("\n--- RESULT ---")
    if success:
        print("Found valid coloring!")
    else:
        print("Failed to find a valid coloring.")
    print("Validity check:", iscoloring(graph, coloring))
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Final conflicts: {final_conflicts}")

    image_filename = visualize_coloring(graph, coloring)
    interactive_data = generate_graph_json(graph, coloring)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    params = {
        "colors": args.colors,
        "steps": args.steps,
        "random": args.random,
        "min_hill_climb": args.min_hill_climb
    }
    results = {
        "elapsed_time": elapsed_time,
        "final_conflicts": final_conflicts,
        "status": success
    }
    card_html = generate_card_html(timestamp, params, results, image_filename)
    update_html_report(card_html, interactive_graph_data=interactive_data)

if __name__ == "__main__":
    main()
