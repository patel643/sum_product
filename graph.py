import numpy as np


class Graph(object):

    '''This class creates undirected graph with adjacency matrix representation
    '''

    def __init__(self, node_list, node_size, edge_u, edge_v, evidence_list,
                 root_idx):
        '''
        :param node_list: list of nodes in the graph
        :type node_list: list of string
        :node_size: number of values each node can take
        :node_size: list of int
        :param edge_u: list containing the name of one end of the edges
        :type edge_u: list of string
        :param edge_v: list containing the name of the other end of the edges,
        edge_u[i] and edge_v[i] gives the ith edge in the graph, the order that
        the edges are defined in the lists doesn't matter
        :param evidence_list: list of observed value for the node, None for
        unobserved nodes
        :type evidence_list: could be numerical values or categorical strings
        '''
        self.node_list = node_list
        self.node_nb = len(self.node_list)
        self.node_size = node_size
        self.evidence_list = evidence_list
        self.adj_matrix = np.zeros((self.node_nb, self.node_nb))
        for i in range(len(edge_u)):
            u = node_list.index(edge_u[i])
            v = node_list.index(edge_v[i])
            self.adj_matrix[u][v] = 1
            self.adj_matrix[v][u] = 1
        self.root = root_idx

    def print_adj_matrix(self):
        print 'adj_matrix'
        print self.adj_matrix
        for i, node in enumerate(self.node_list):
            print 'node %d has neighbors' % i
            print self.neighbor(i)

    def neighbor(self, node_idx):
        '''find neighbors of a node'''
        neighbors = []
        for j, value in enumerate(self.adj_matrix[node_idx]):
            if value == 1:
                neighbors.append(j)
        return neighbors
