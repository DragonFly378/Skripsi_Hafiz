import numpy as np
import igraph as ig

class mincut_segmentation:
    def __init__(self, edges, weights):
        self.edges = edges
        self.weights = weights
        self.G_0 = None
        self.G = None
        self.node_a = None
        self.n_nodes = None

        self.best_value = float('inf')
        self.cut_weight = None

        self.node_s = None
        self.node_t = None

        self.in_pq = []
        self.node_pq = []
        
        # self.calc_mincut()

    def build_graf(self, cols, rows):
        self.G_0 = ig.Graph(cols * rows + 1)


    def calc_mincut(self):
        print("Informasi vertices:")
        # Point 2 from paper
        self.G = self.G_0.copy()  
        self.G.add_edges(self.edges)
        self.G.es['weight'] = np.zeros(len(self.edges))
        self.G.es['weight'] = self.weights

        print('total edges graf: ',self.G.ecount())
        print('total node graf: ', self.G.vcount())

        # Point 3 from paper
        self.node_a = self.G_0.vs[0]
        self.n_nodes = self.G_0.vcount()
        self.all_nodes = np.array(self.G_0.vs)
        self.best_cut = []
        print(self.node_a)
        print(self.n_nodes)

        self.node_t = self.node_a
        
        while (self.n_nodes >= 2):
            # Phase 5 from paper
            # Phase 6 from paper
            for node in self.all_nodes:
                if (node != self.node_a):
                    self.node_pq.append(0)
                    self.in_pq.append(True)

            self.n_nodes -= 1
        print(len(self.node_pq))



    
    

