// Struktur Data LinkedList
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
 				this->backgroundProbability = backgroundProbability;
				
 				this->parent = nullptr;
 			}
 	}



