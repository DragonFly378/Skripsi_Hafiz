import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def construct_graph(image):
    height, width = image.shape[:2]
    num_pixels = height * width

    # Create an empty graph
    graph = nx.Graph()

    # Add nodes to the graph
    graph.add_nodes_from(range(num_pixels))


    # # Visualize the graph (optional)
    # nx.draw(graph, with_labels=True)
    # plt.show()

    # Define connectivity (8-connectivity)
    dx = [-1, 0, 1, -1, 1, -1, 0, 1]
    dy = [-1, -1, -1, 0, 0, 1, 1, 1]

    # Add edges and compute weights
    for y in range(height):
        for x in range(width):
            node = y * width + x

            # Connect with neighboring pixels
            for i in range(8):
                nx = x + dx[i]
                ny = y + dy[i]

                if 0 <= nx < width and 0 <= ny < height:
                    neighbor_node = ny * width + nx

                    # Compute edge weight based on pixel similarity (e.g., intensity/color difference)
                    edge_weight = compute_edge_weight(image[y, x], image[ny, nx])

                    # Add edge between current node and neighbor node with computed weight
                    graph.add_edge(node, neighbor_node, weight=edge_weight)

    return graph

# def compute_edge_weight(pixel1, pixel2):
#     # Compute edge weight based on pixel similarity (e.g., intensity/color difference)
#     # You can define your own method here based on the specific application requirements
#     return np.abs(pixel1 - pixel2)  # Example: Absolute intensity difference

# Example usage
image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Construct the graph
graph = construct_graph(image)

# # Specify the source and sink nodes
# source_node = 0
# sink_node = 8

# # Find the shortest path using breadth-first search
# shortest_path = nx.shortest_path(graph, source=source_node, target=sink_node)

# # Create a tree from the shortest path
# tree = nx.Graph()
# for i in range(len(shortest_path) - 1):
#     tree.add_edge(shortest_path[i], shortest_path[i + 1])

# # Print the shortest path and the edges of the resulting tree
# print("Shortest path:", shortest_path)
# print("Tree edges:", tree.edges())

# # Visualize the image, graph, shortest path, and tree (optional)
# plt.subplot(2, 2, 1)
# plt.imshow(image, cmap='gray')
# plt.title("Image")

# plt.subplot(2, 2, 2)
# nx.draw(graph, with_labels=True)
# plt.title("Graph")

# plt.subplot(2, 2, 3)
# plt.imshow(image, cmap='gray')
# plt.plot(np.array(shortest_path) % image.shape[1], np.array(shortest_path) // image.shape[1], 'r-')
# plt.title("Shortest Path")

# plt.subplot(2, 2, 4)
# nx.draw(tree, with_labels=True)
# plt.title("Tree")

# plt.tight_layout()
# plt.show()
