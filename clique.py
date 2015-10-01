from potential import Potential


class Clique(object):
    def __init__(self, id, nodes, sizes, values=None):
        self.id = id
        self.potential = Potential(nodes, sizes, values)

    def enter_evidence(self, evidence):
        self.potential.enter_evidence(evidence)
