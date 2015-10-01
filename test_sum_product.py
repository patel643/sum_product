
from clique import Clique
import numpy as np
from graph import Graph
from model import Model
from clique import Clique

if __name__ == '__main__':
    node_nb = 3
    node_list = ['x1', 'x2', 'x3']
    edge_u = ['x1', 'x2']
    edge_v = ['x2', 'x3']
    ns = 2 * np.ones(node_nb)
    # evidence = ['G', 'C', 'A', 'T', 'T', None, None, None, None, None]
    evidence = [None, None, None]
    root_idx = 2
    tester_graph = Graph(node_list, ns, edge_u, edge_v, evidence, root_idx)
    tester_graph.print_adj_matrix()

    #define cliques
    phi_1 = np.array([0.9, 0.1])
    phi_one = np.array([1, 1])
    phi_12 = np.array([[0.9, 0.1], [0.2, 0.8]])
    phi_23 = np.array([[0.9, 0.1], [0.7, 0.3]])
    phi_2 = phi_one
    phi_3 = phi_one
    # all single nodes and all pairs of nodes connected by edge
    clique_nodes = [[0], [1], [2], [0, 1], [1, 2]]
    cliques = []
    cliques.append(Clique(0, clique_nodes[0], np.array([2]), phi_1))
    cliques.append(Clique(1, clique_nodes[1], np.array([2]), phi_2))
    cliques.append(Clique(2, clique_nodes[2], np.array([2]), phi_3))
    cliques.append(Clique(3, clique_nodes[3], np.array([2, 2]), phi_12))
    cliques.append(Clique(4, clique_nodes[4], np.array([2, 2]), phi_23))
    #model
    tester_model = Model(tester_graph, cliques, evidence)
    tester_model.print_model()
    #""Execute sum_product algorithm""
    tester_model.sum_product()
    #Print out the marginal probability of each node.
    #marginal = net.marginal_nodes([C])
    #print 'Probability it is cloudy:     ', marginal.T[1]*100, '%'
    #marginal = net.marginal_nodes([S])
    #print 'Probability the sprinkler is on:  ', 0, '%'   #Observed node
    #marginal = net.marginal_nodes([R])
    #print 'Probability it is raining:      ',marginal.T[1]*100, '%'
    #marginal = net.marginal_nodes([W])
    #print 'Probability the grass is wet:  ', marginal.T[1]*100, '%'"
