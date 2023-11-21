#include <iostream>
#include <vector>
#include <algorithm>
#include <map>

using namespace std;


class Node {
public:
    char name;
    int data;
    int capacity; // Capacity of the edge between this node and its parent
    Node* parent;
    vector<Node*> children;
    map<Node*, int> edges; // Map to store child nodes and their capacities


    Node(char name) {
        this->name = name;
        parent = nullptr;
        // capacity = 0; // Initialize capacity to 0
    }
};

class Tree {
private:
    Node* root;
public:
    Tree() {
        root = nullptr;
    }

    void insertChild(Node* current, Node* next, int capacity) {
        Node* rootOfCurrent = getRoot(current);
        Node* rootOfNext = getRoot(next);

        if(next->parent == nullptr || rootOfNext->name == rootOfCurrent->name){

            next->parent = current;
            current->edges[next] = capacity;
            current->children.push_back(next);

            // get root of each node
            Node* nextRoot = getRoot(next);        
            cout << "node " << next->name 
			<< " masuk ke tree " 
			<< nextRoot->name ;
            cout << endl;

        }else if (rootOfNext->name != rootOfCurrent->name){
            cout << endl << "ada path di: "
			<< next->name << endl;
            cout << "path nya adalah: "<< endl; 
            getPath(current, next);
            cout << "masuk ke tahap augmentasi" 
			<< endl << endl;
        }  
        
    }

    // Add this helper function to get the capacity between two nodes
    int getEdgeCapacity(Node* parent, Node* child) {
        // Find the edge connecting the parent and child nodes
        auto it = parent->edges.find(child);
        if (it != parent->edges.end()) {
            return it->second; // Return the capacity of the edge
        }

        // for (size_t i = 0; i < parent->children.size(); i++) {
        //     if (parent->children[i] == child) {
        //         return child->capacity; // Return the capacity of the edge
        //     }
        // }
        return 0; // Return 0 if the edge is not found (should not happen if the tree is correctly constructed)
    }
    

    void display(Node* node, int depth = 0) {

        if (node == nullptr)
            return;

        // Print current node with indentation
        for (int i = 0; i < depth; ++i) {
            cout << "    ";
        }
        cout << "|-- " << node->name << " (Capacity: " << node->capacity << ")" << endl;

        // Recursively display children
        for (Node* child : node->children) {
            display(child, depth + 1);
        }
    }

    void displayTree(Node* root) {
        cout << endl << "Tree dari Search Node " 
	    << root->name << " adalah: " << endl;
        display(root);
    }
 
    Node* getRoot(Node* child) {
 
        Node* current = child;
        while (current->parent != nullptr) {
            current = current->parent;
        }

        return current;
    }

    vector<Node*> getLeafNodes(Node* node) {
        vector<Node*> leafNodes;

        if (node == nullptr){
            return leafNodes;
        }

        if (node->children.empty()) {
            leafNodes.push_back(node);
        } else {
            for (Node* child : node->children) {
                vector<Node*> childLeafNodes = 
				getLeafNodes(child);

                leafNodes.insert(
				leafNodes.end(), 
				childLeafNodes.begin(), 
				childLeafNodes.end()
				);
            }
        }        
        return leafNodes;
    }

    void displayLeafNodes(Node* root) {
        vector<Node*> leafNodes = getLeafNodes(root);
        cout << "Leaf nodes: ";
        for (Node* leafNode : leafNodes) {
            cout << leafNode->name << " ";
        }
        cout << endl;
    }
    
    bool getPathToRoot(Node* leaf, 
	vector<char>& path) {
        if (leaf == nullptr)
            return false;

        Node* current = leaf;
        while (current != nullptr) {
            path.push_back(current->name);
            current = current->parent;
        }

        return true;
    }
    
    vector<char> getPathFromLeafToRoot(Node* leaf) {
        vector<char> path;
        getPathToRoot(leaf, path);
        return path;
    }

    void displayLeafToRoot ( Node* leaf) {
        vector<char> path = 
		getPathFromLeafToRoot(leaf);
        getPathToRoot(leaf, path);

        // Display the path
        if(path[path.size()-1] != 't'){
            reverse(path.begin(), path.end());
        }
        cout << "Path from leaf " << leaf->name 
		<< " to root:" << endl;
        for (int i = 0; i < path.size(); i++) {
            cout << path[i];
            if(i != path.size() -1){
                cout<< "->";
            }
        }
        cout << endl;
    }

    void getPath(Node* current, Node* next){
        vector<char> tmp_current = 
		getPathFromLeafToRoot(current);
        vector<char> tmp_next = 
		getPathFromLeafToRoot(next);
        vector<char> path;
        int totalCapacity = 0;

        for (char cek : tmp_current){
            cout<< cek ;
        };

        cout<<endl;

        for (char cek2 : tmp_next){
            cout<< cek2;
        };

        cout<< endl;



        if(tmp_current[tmp_current.size() - 1] == 't'){

            reverse(tmp_next.begin(), tmp_next.end());

            for(char node : tmp_next){
                path.push_back(node);
                if (path.size() > 1) {
                    Node* parent = next->parent;
                    int capacity = getEdgeCapacity(parent, next);
                    totalCapacity += capacity;
                    cout << "Capacity from " << parent->name << " to " << next->name << ": " << capacity << endl;
                }
            }
            for(char node : tmp_current){
                path.push_back(node);
                if (path.size() > 1) {
                    Node* parent = current->parent;
                    int capacity = getEdgeCapacity(parent, current);
                    totalCapacity += capacity;
                    cout << "Capacity from " << parent->name << " to " << next->name << ": " << capacity << endl;
                }
            }
        }else{
            
            reverse(tmp_current.begin(), tmp_current.end());

            for(char node : tmp_current){
                path.push_back(node);
                if (path.size() > 1) {
                    Node* parent = current->parent;
                    int capacity = getEdgeCapacity(parent, current);
                    totalCapacity += capacity;
                    cout << "Capacity from cu " << parent->name << " to " << current->name << ": " << capacity << endl;
                }
            }
            for(char node : tmp_next){
                path.push_back(node);
                if (path.size() > 1 && next->parent != nullptr) {
                    Node* parent_tmp = next->parent;
                    // cout<< parent->name;
                    int capacity = getEdgeCapacity(parent_tmp, next);
                    totalCapacity += capacity;
                    cout << "Capacity from ci " << parent_tmp->name << " to " << next->name << ": " << capacity << endl;
                    next = parent_tmp;
                }
            }
        }
        for (char i : path) {
            cout << i;
            // if(i != path.size() -1){
            //     cout<< "->";
            // }
        }

        cout << endl;
        // Print total capacity
        // cout << "Total Capacity along the path: " << totalCapacity << endl;
    }
};

int main() {
	// Create Tree S and T
	Tree tree;
	// Tree tree;
	// Create root node s and t
	Node* root_S = new Node('s');
	Node* root_T = new Node('t');

	Node* nodeA = new Node('a');
	Node* nodeB = new Node('b');
	Node* nodeC = new Node('c');
	Node* nodeH = new Node('h');
	Node* nodeG = new Node('g');
	Node* nodeF = new Node('f');
	Node* nodeI = new Node('i');
	Node* nodeJ = new Node('j');
    Node* nodeK = new Node('k');


    // Set the edge capacities
    // int capacity_SA = 10;
    // int capacity_SB = 15;
    // int capacity_SC = 5;
    // int capacity_TI = 12;
    // int capacity_AH = 7;
    // int capacity_BG = 9;
    // int capacity_CF = 8;
    // int capacity_IH = 6;
    // int capacity_IJ = 11;

    tree.insertChild(root_S, nodeA, 3);
    tree.insertChild(root_S, nodeB, 4);
    tree.insertChild(root_S, nodeC, 2);
    tree.insertChild(root_T, nodeI, 7);
    tree.insertChild(nodeA, nodeH, 12);
    tree.insertChild(nodeA, nodeG, 5);
    tree.insertChild(nodeB, nodeG, 11);
    tree.insertChild(nodeC, nodeF, 22);
    tree.insertChild(nodeI, nodeK, 8);
    // tree.insertChild(nodeH, nodeK, 10);
    // tree.insertChild(nodeI, nodeJ, 9);

    // tree.display(nodeH);

    // Display the root node's name'
    // Node* rootOfTree = tree.getRoot(nodeB);
    // cout << "Root of tree from nodeB: " << rootOfTree->name << endl;

    tree.getPath(root_S, nodeH);

    // int cap2 = tree.getEdgeCapacity(nodeA, nodeG);
    // cout << " Capacity between nodeA and nodeG: " << cap2 << endl;

    // int cap = tree.getEdgeCapacity(nodeB, nodeG);
    // cout << " Capacity between nodeB and nodeG: " << cap << endl;


   return 0;
}
