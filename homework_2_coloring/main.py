# main.py

import argparse
import time
import os
from datetime import datetime
from graph import load_graph
from local_search import color, iscoloring, count_conflicts_cpu, count_conflicts_gpu

def update_html_report(card_html, html_file="coloring.html"):
    """
    Insert the card_html content into the html_file.
    If the file doesn't exist, create a new one with a header and footer.
    Otherwise, insert the card before the closing </body> tag.
    """
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Insert before closing </body>
        if "</body>" in content:
            content = content.replace("</body>", f"{card_html}\n</body>")
        else:
            content += card_html
    else:
        # Create a new HTML document with header, style and footer.
        content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Graph Coloring Homework - Daniel Král</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 20px;
      background-color: #f5f5f5;
    }}
    .card {{
      border: 2px solid #008CBA;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 20px;
      box-shadow: 2px 2px 12px rgba(0, 140, 186, 0.2);
      background-color: #e0f7fa;
    }}
    .card.failure {{
      border-color: #e53935;
      background-color: #ffebee;
    }}
    h1 {{
      color: #0077b6;
    }}
    .card h2 {{
      margin-top: 0;
    }}
    @media print {{
      body {{
        background: none;
      }}
    }}
  </style>
</head>
<body>
  <h1>Graph Coloring Homework - Daniel Král</h1>
  {card_html}
</body>
</html>
"""
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"HTML report updated: {html_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Graph Coloring via local search with optional GPU acceleration."
    )
    parser.add_argument("file", help="Path to .col graph file (e.g., dsjc125.9.col)")
    parser.add_argument("--colors", type=int, default=44, help="Number of colors to use (default: 44)")
    parser.add_argument("--steps", type=int, default=100000, help="Maximum number of local search steps")
    parser.add_argument("--random", type=float, default=0.3, help="Probability for random walk moves (default: 0.3)")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU acceleration for conflict counting")
    args = parser.parse_args()

    # Load the graph.
    graph = load_graph(args.file)
    print(f"Graph loaded: {graph.num_vertices} vertices, {graph.edges.shape[0]} edges")

    # Check GPU availability (if requested).
    if args.gpu:
        try:
            from numba import cuda
            if cuda.is_available():
                print("GPU acceleration enabled.")
            else:
                print("GPU acceleration requested but CUDA support is not available. Using CPU.")
        except ImportError:
            print("Numba CUDA not installed. Using CPU.")

    # Run the local search algorithm and measure the elapsed time.
    start_time = time.time()
    coloring, success = color(graph, args.colors, args.steps, use_gpu=args.gpu, random_walk_prob=args.random)
    elapsed_time = time.time() - start_time

    # Compute final conflict count using the appropriate conflict counting function.
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

    # Prepare the HTML card.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    card_class = "card" if success else "card failure"
    card_html = f"""
  <div class="{card_class}">
    <h2>Run at {timestamp}</h2>
    <p><strong>Parameters:</strong></p>
    <ul>
      <li>Colors attempted: {args.colors}</li>
      <li>Steps allowed: {args.steps}</li>
      <li>Random walk probability: {args.random}</li>
    </ul>
    <p><strong>Results:</strong></p>
    <ul>
      <li>Elapsed time: {elapsed_time:.2f} seconds</li>
      <li>Final conflicts: {final_conflicts}</li>
      <li>Status: {"Valid coloring" if success else "Invalid coloring"}</li>
    </ul>
  </div>
    """
    # Update the HTML report.
    update_html_report(card_html)

if __name__ == "__main__":
    main()
