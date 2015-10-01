import numpy as np
from util import find


class Potential(object):

    '''potential class
    '''

    def __init__(self, nodes_idx=[], sizes=np.array([1]), values=None):
        '''
        :param nodes_idx: a list of related nodes that defines the potential
        :param sizes: A list of the node sizes corresponding to the nodes in
        the 'nodes' list
        :param values: an array contains the value of potentials
        in the format of: size of node1 * size of node2...
        :type values: multidim Numpy ndarray, dimension = len(nodes_idx)
        number of values in each dimension i = size[i]
        '''
        self.nodes_idx = nodes_idx
        self.sizes = sizes
        if values is None:
            sizes = np.array(sizes, dtype='int').tolist()
            self.values = np.ones(sizes)
        else:
            self.values = values

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return ((self.sizes == other.sizes).all() and
                (self.nodes_idx == other.nodes_idx)
                and np.allclose(self.values, other.values))

    def enter_evidence(self, evidence=None, print_opt=False):
        '''take the slice of potential table that contains the observed value
        1) change the node size to 1
        2) take the slice of the potenital table
        :param evidence: a list of index of values of observed nodes,
        one value for each node, is None if the node is not observed
        length of evidence list must be equal to the nodes number
        '''

        obs_node_ids = []
        obs_nodes_index = []  # index for observed nodes in self.nodes list,
        # also the dimension number that the probability is stored in the values
        # matrix
        obs_values_index = []
        # which values that the observed node takes
        for i, nd_id in enumerate(self.nodes_idx):
            if evidence[nd_id] is not None:
                obs_nodes_index.append(i)
                obs_values_index.append(evidence[nd_id])
                obs_node_ids.append(nd_id)
        index = self.mk_multi_index(len(self.nodes_idx), obs_nodes_index,
                                    obs_values_index)
        self.values = self.values[index]
        if print_opt:
            print 'observed nodes id'
            print obs_node_ids
            print 'index of the observed nodes in the clique potential node list'
            print obs_nodes_index
            print ''''index of the values that the observed nodes have, in the order the
            lookup table is indexed'''
            print obs_values_index
            print 'conditioned slice of the multidimensional lookup table'
            print self.values
        self.sizes[obs_nodes_index] = 1

    def mk_multi_index(self, n, dims, vals):
        """
        Creates a list of slices, named index. The list can be used to slice an
        array, for example:
            index = mk_multi_index(3, [0, 2], [3, 2])
            gives index = [slice(3,4), slice(None), slice(2, 3)],
            which will select out dim 0 the 3rd entry, out of dim 1 everything,
            and out of dim 2 the 2nd entry.

            So if A[:,:,1]=[[1 2], [3 4], [5 6]]
                A[:,:,2]=[[7 8], [9 10], [11 12]]

            then A(index{:}) = [11 12].

        Parameters
        ----------
        n: Int
            The number of dimensions the matrix to be sliced has.

        dims: List
            The dimensions we wish to slice from.

        vals: List
            Which entries to select out of the desired dimensions.

        """
        index = []
        for i in range(0, n):
            if i in dims:
                val = vals[dims.index(i)]
                index.append(slice(val, val + 1))
            else:
                index.append(slice(None))
        return index

    def copy(self):
        """
        Creates a fresh copy of this potential.
        """
        new_pot = dpot(self.domain, self.sizes, self.T)
        new_pot.observed_domain = self.observed_domain[:]
        return new_pot

    def multiply(self, pot, print_opt=False):
        """
        Perfrom multiplication between
        this potential and another.
        ASSUMING: the potential are either singleton or pair of nodes
        Extend the domain of the potential with the smaller domain
        so that both have the same domain.
        """
        if print_opt:
            print 'multiply'
        to_ret = Potential()
        if len(self.sizes) == 2 or len(pot.sizes) == 2:
            if len(self.sizes) == 1:
                smaller_pot = self
                larger_pot = pot
            elif len(pot.sizes) == 1:
                smaller_pot = pot
                larger_pot = self
            else:
                print 'not defined'
                print len(self.sizes)
                print len(pot.sizes)
            dim = []
            for i in smaller_pot.nodes_idx:
                dim.append(larger_pot.nodes_idx.index(i))

            sz = np.ones((1, len(larger_pot.nodes_idx)), dtype='int')
            sz[0, dim] = smaller_pot.sizes
            sz = sz.tolist()
            sz = sz[0]
            Ts = smaller_pot.values.reshape(sz)
            for i in xrange(0, len(larger_pot.sizes)):
                if (i not in dim):
                    Ts = np.repeat(Ts, larger_pot.sizes[i], i)
            values = larger_pot.values * Ts
            if print_opt:
                print 'reshaped value table'
                print Ts
                print 'result value'
                print larger_pot.values
                print 'new nodes_idx'
                print larger_pot.nodes_idx
                print Potential(larger_pot.nodes_idx, larger_pot.sizes, values)
            to_ret = Potential(larger_pot.nodes_idx, larger_pot.sizes, values)
        else:
            values = self.values * pot.values
            to_ret = Potential(self.nodes_idx, self.sizes, values)
        return to_ret

    def marginalize(self, onto_node, print_opt=False):
        '''marginalize a node out by summing over its values

        :param node_onto:
            the node that are left after marginalization
            the index of the node in the graph, which is the
        node_id.index(node_index) th node in the potential
        '''
        assert isinstance(onto_node, list), 'onto_node for marginalize must be\
        a list'
        ns = np.zeros((1, np.max(self.nodes_idx)+1))
        ns[0, self.nodes_idx] = self.sizes
        sum_over = np.setdiff1d(np.array(self.nodes_idx), np.array(onto_node))
        if print_opt:
            print 'marginalize'
            print 'potential has nodes:'
            print self.nodes_idx
            print 'marginalize onto nodes:'
            print onto_node
            print 'so sum over nodes:'
            print sum_over
        # find out which dimension to sum out
        #dim_of_node_to_marg = self.noded_id.index(sum_over)
        ndx = []
        smallT = self.values
        for i in sum_over:
            temp = find(np.array([np.array(self.nodes_idx) == i]))
            if print_opt:
                print 'its the dimension'
                print temp
            if temp.shape != (1,):
                ndx.append(temp[0, 0])
        ndx = np.array(ndx)
        for i in xrange(0, len(ndx)):
            if ndx[i] < smallT.ndim:
                """Sum over the dimension ndx[i]"""
                smallT = np.sum(smallT, ndx[i])
                """Compensate for reduced dimensions of smallT"""
                ndx = ndx - 1
        smallpot = Potential(onto_node, ns[0, onto_node], smallT)
        return smallpot

    def normalize(self):
        sum = np.sum(self.values)
        self.values = [x/sum for x in self.values]
