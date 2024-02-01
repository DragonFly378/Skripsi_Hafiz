import igraph as ig
import numpy as np

# Adding edges
edges = []
source = 0
tmp = np.array([1,2,3,4,5,6,7])
sink = tmp.size

edges.extend(list(zip([source] * tmp.size, tmp)))
edges.extend(list(zip([sink] * tmp.size, tmp)))

print(edges)

# Create a graph with specifying the number of vertices
graph = ig.Graph(tmp.size + 2)

# Add edges dynamically, which will add vertices as needed
graph.add_edges(edges)

# Displaying information about edges
print("Information about edges:")
for edge in graph.es:
    print(f"Source: {edge.source}, Target: {edge.target}")
