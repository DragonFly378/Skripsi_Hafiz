#include <iostream>
#include <vector>
using namespace std;


class Node {
    public:

        string name;
        int data;
        Node* parent;
        vector<Node*> children;

        Node(string name, int data ) {
            this->name  = name;
            this->data = data;       
            this->parent = nullptr;
        }
}

class Tree {
private:
    Node* root;
public:
    Tree() {
        root = nullptr;
    }

    Node* createNode(string name, int data) {
        Node* newNode = new Node(name, data);
        return newNode;
    }

    void insertChild(Node* parent, Node* child) {
        if (parent == nullptr || child == nullptr)
            return;

        child->parent = parent;
        parent->children.push_back(child);
    }

    void display(Node* node, int depth = 0) {
        if (node == nullptr)
            return;

        // Print current node with indentation
        for (int i = 0; i < depth; ++i) {
            cout << "    ";
        }
        cout << "|-- " << node->name << endl;

        // Recursively display children
        for (Node* child : node->children) {
            display(child, depth + 1);
        }
    }

    void displayTree() {
        display(root);
    }
};

int main() {
    Tree tree;

	Node* root = tree.createNode(S, 0);
    Node* child1 = tree.createNode(A, 12);
    Node* child2 = tree.createNode(B, 2);
    Node* child3 = tree.createNode(C, 3);
    Node* child4 = tree.createNode(D, 4);
    // Node* child5 = tree.createNode(5);
    // Node* child6 = tree.createNode(6);
    // Node* child7 = tree.createNode(7);  
    // Node* child8 = tree.createNode(8);  


    tree.insertChild(root, child1);
    tree.insertChild(root, child2);
    tree.insertChild(child1, child3);
    tree.insertChild(child2, child4);

    tree.display(root);

    return 0;
}
