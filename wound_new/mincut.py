import numpy as np
import igraph as ig
from tqdm import tqdm

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

        self.node_pq = None
        
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
        self.n_nodes = self.G_0.vcount()
        self.all_nodes = np.array(self.G_0.vs)
        self.best_cut = []
        print(self.node_a)
        print(self.n_nodes)
        self.in_pq = [False] * self.n_nodes

        self.node_t = self.node_a
        
        # while_progress_bar = tqdm(total=self.n_nodes, desc="Outer Loop", unit="Iteration")
        for node in range(self.n_nodes, -1, -1):
            # Phase 5 from paper
            # Phase 6 from paper     
            # self.node_a = self.G_0.vs[0].index


            # for_progress_bar = tqdm(range(self.n_nodes), desc="Inner Loop", unit="Iteration")
            print(node)
            for node in range(self.n_nodes):
                if not self.in_pq[node]:
                    self.node_pq = 0
                    self.in_pq[node] = True
                # print(node)
            # for_progress_bar.update(1)
                # for edge in self.G.es:
            # for_progress_bar.close() 
            # while_progress_bar.update(1)
        # while_progress_bar.close()
        # print(len(self.node_pq))



    
    

