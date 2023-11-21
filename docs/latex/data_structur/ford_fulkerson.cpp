#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class Edge {
public:
    int to;
    int capacity;
    int flow;

    Edge(int to, int capacity) : to(to), capacity(capacity), flow(0) {}
};

class FordFulkerson {
private:
    int numNodes;
    vector<vector<Edge>> graph;

public:
    FordFulkerson(int numNodes) : numNodes(numNodes) {
        graph.resize(numNodes);
    }

    void addEdge(int from, int to, int capacity) {
        graph[from].emplace_back(to, capacity);
        graph[to].emplace_back(from, 0); // Backward edge with initial flow 0
    }

    // Find augmenting path using BFS
    bool findAugmentingPath(int source, int sink, vector<int>& parent) {
        parent.assign(numNodes, -1);
        queue<int> q;
        q.push(source);
        parent[source] = -2;

        while (!q.empty()) {
            int current = q.front();
            q.pop();

            for (const Edge& edge : graph[current]) {
                int next = edge.to;
                if (parent[next] == -1 && edge.capacity > edge.flow) {
                    parent[next] = current;
                    if (next == sink)
                        return true;
                    q.push(next);
                }
            }
        }

        return false;
    }

    // Ford-Fulkerson algorithm
    int maxFlow(int source, int sink) {
        int maxFlow = 0;
        vector<int> parent;

        while (findAugmentingPath(source, sink, parent)) {
            int pathFlow = INT_MAX;
            int current = sink;

            // Find the minimum flow along the augmenting path
            while (current != source) {
                int prev = parent[current];
                for (const Edge& edge : graph[prev]) {
                    if (edge.to == current) {
                        pathFlow = min(pathFlow, edge.capacity - edge.flow);
                        break;
                    }
                }
                current = prev;
            }

            // Update the flow in the graph along the augmenting path
            current = sink;
            while (current != source) {
                int prev = parent[current];
                for (Edge& edge : graph[prev]) {
                    if (edge.to == current) {
                        edge.flow += pathFlow;
                        break;
                    }
                }
                // Add backward edge for residual graph
                for (Edge& edge : graph[current]) {
                    if (edge.to == prev) {
                        edge.flow -= pathFlow;
                        break;
                    }
                }
                current = prev;
            }

            maxFlow += pathFlow;
        }

        return maxFlow;
    }
};

int main() {
    int numNodes = 6;
    FordFulkerson graph(numNodes);

    // Example: Add edges to the graph
    graph.addEdge(0, 1, 16);
    graph.addEdge(0, 2, 13);
    graph.addEdge(1, 2, 10);
    graph.addEdge(1, 3, 12);
    graph.addEdge(2, 1, 4);
    graph.addEdge(2, 4, 14);
    graph.addEdge(3, 2, 9);
    graph.addEdge(3, 5, 20);
    graph.addEdge(4, 3, 7);
    graph.addEdge(4, 5, 4);

    int source = 0;
    int sink = 5;
    int maxFlow = graph.maxFlow(source, sink);
    cout << "Maximum Flow from node " << source << " to node " << sink << ": " << maxFlow << endl;

    return 0;
}
