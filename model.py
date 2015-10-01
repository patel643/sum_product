from potential import Potential
import numpy as np


class Model(object):

    def __init__(self, graph, cliques, evidence):
        '''undirected probability graphical model: only implemented for
        undirected trees
        :param cliques: all single nodes and pairs of node of all edges
        '''
        self.graph = graph
        self.cliques = cliques
        self.evidence = evidence
        self.initalize_message()

    def initalize_message(self):
        '''every node has a message dictionary
        self.message ={j: {nodek: mkj(xj), nodeh: mhj(xj), ...},
                       i: {nodek: mki(xi), nodeh: mhi(xi), ...},
                       }
        '''
        self.message = {}
        for node_idx, node_name in enumerate(self.graph.node_list):
            self.message[node_idx] = {}
            for neighbor_node in self.graph.neighbor(node_idx):
                self.message[node_idx][neighbor_node] = Potential(
                    [node_idx], np.array([self.graph.node_size[node_idx]]),
                    np.ones(self.graph.node_size[node_idx]))

    def get_clique(self, nodes_idx):
        '''from a list of cliques
        get the id of the clique that contains the nodes
        in nodes.
        '''
        for clique in self.cliques:
            if set(clique.potential.nodes_idx) == set(nodes_idx):
                return clique
        print 'no clique containes these nodes:'
        print nodes_idx
        return None

    def print_model(self):
        self.graph.print_adj_matrix
        for clique in self.cliques:
            print 'clique %d' % clique.id
            print clique.potential.nodes_idx
            print clique.potential.sizes
            print clique.potential.values
        print self.evidence

    def sum_product(self):
        """
        belief propogation using sum_product algorithm
        """
        if self.evidence is not None:
            self.enter_evidence()
        # phase 1: messages flow from leaf to root
        root = self.graph.root
        for neighbor in self.graph.neighbor(root):
            self.collect(root, neighbor)
        for neighbor in self.graph.neighbor(root):
            self.distribute(root, neighbor)
        self.nodeMarginal = {}
        for node_idx, node in enumerate(self.graph.node_list):
            self.nodeMarginal[node] = self.compute_marginal(node_idx)
        print self.nodeMarginal

    def enter_evidence(self):
        for clique in self.cliques:
            print 'enter evidence for clique %d\n with nodes %r' % (
                clique.id,
                clique.potential.nodes_idx)
            clique.enter_evidence(self.evidence)
        self.print_model()

    def collect(self, nodei, nodej):
        print 'collect node%d node%d' % (nodei, nodej)
        for nodek in self.graph.neighbor(nodej):
            if nodek is not nodei:
                self.collect(nodej, nodek)
        self.send_message(nodei, nodej)

    def distribute(self, nodei, nodej):
        '''distribute from i to j'''
        print 'distribute from  node%d to node%d' % (nodei, nodej)
        self.send_message(nodej, nodei)
        for nodek in self.graph.neighbor(nodej):
            if nodek is not nodei:
                self.distribute(nodej, nodek)

    def send_message(self, nodei, nodej, print_opt=False):
        '''send message from j to i:
        calculate message_ji: get a potential at j by taking the product
        over all potentials that reference xj and summing over xj
        mji(xi) = sum_xj (phiE_xj, phi(xi, xj), product(mkj))
        sending the message: node_i.potential = message_ji * node_i.potential
        '''
        ij_clique = self.get_clique([nodei, nodej])
        j_clique = self.get_clique([nodej])
        print 'send message from node %d to node %d' % (nodej, nodei)
        message_ji = self.message[nodei][nodej]
        temp = j_clique.potential.multiply(ij_clique.potential)
        message_ji = message_ji.multiply(temp)
        for key in self.message[nodej].keys():
            if key is not nodei:
                message_ji = message_ji.multiply(self.message[nodej][key])
        message_ji = message_ji.marginalize([nodei])
        self.message[nodei][nodej] = message_ji

    def compute_marginal(self, nodei):
        i_clique = self.get_clique([nodei])
        p_nodei = i_clique.potential
        for neighbor in self.graph.neighbor(nodei):
            p_nodei = p_nodei.multiply(self.message[nodei][neighbor])
        p_nodei.normalize()
        return p_nodei
