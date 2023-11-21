// Struktur Data Tree
class Node {
    public:
        bool isForeground;
        double foregroundProbability;
        double backgroundProbability;
        vector<GaussianComponent> gmmComponents;

        Node* parent;
        vector<Node*> children;

        Node(bool isForeground, 
                double foregroundProbability, 
                double backgroundProbability ) {

            this->isForeground = isForeground;
            this->foregroundProbability = foregroundProbability;
            this->backgroundProbability = backgroundProbability;;
            
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

        Node* createNode(
            bool isForeground, 
            double foregroundProbability, 
            double backgroundProbability) {

            Node* newNode = new Node(
                isForeground, 
                foregroundProbability, 
                backgroundProbability);
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
        cout << "|-- " << node->data << endl;

        // Recursively display children
        for (Node* child : node->children) {
            display(child, depth + 1);
        }
    }
};

int main() {
    Tree tree;

    Node* root = tree.createNode(0);
    Node* child1 = tree.createNode(1);
    Node* child2 = tree.createNode(2);
    Node* child3 = tree.createNode(3);
    Node* child4 = tree.createNode(4);
    Node* child5 = tree.createNode(5);
    Node* child6 = tree.createNode(6);
    Node* child7 = tree.createNode(7);  
    Node* child8 = tree.createNode(8);  



    tree.insertChild(root, child1);
    tree.insertChild(root, child2);
    tree.insertChild(child1, child3);
    tree.insertChild(child2, child4);
    tree.insertChild(child2, child5);
    tree.insertChild(child3, child6);
    tree.insertChild(child3, child7);
    tree.insertChild(child3, child8);

    tree.display(root);

    return 0;
}
