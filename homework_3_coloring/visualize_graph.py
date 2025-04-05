import os                           
import time                         
import matplotlib.pyplot as plt
import networkx as nx

def visualize_coloring(graph, colors):
    """
    Converts the graph (from our custom Graph object) into a NetworkX graph,
    then draws it using the provided coloring. The resulting image is saved
    as a JPG file in the "images" folder with a unique name, and the filename is returned.
    """
    G = nx.Graph()
    G.add_nodes_from(range(graph.num_vertices))
    for u, v in graph.edges:
        G.add_edge(u, v)
    
    cmap = plt.get_cmap("tab20")
    node_colors = [cmap(color % 20 / 20) for color in colors]
    
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=300, font_size=8)
    plt.title("Graph Coloring Visualization")
    
    output_dir = "images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = os.path.join(output_dir, f"graph_coloring_{int(time.time())}.jpg")
    
    plt.savefig(filename, format="jpg")
    plt.close()
    
    return filename