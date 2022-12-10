from edge_def import Edge as E
from node_def import Node as N

class Graph:
    def __init__(self, nodes=dict(), edges=list()):
        self.nodes = nodes
        self.edges = edges

    def all_nodes(self):
        return set([n.label for n in self.nodes])


    def __repr__(self):
        nums = "nodes: %s, edges: %s\n" % (len(self.nodes), len(self.edges))
        return nums + "\n".join(["%d:\t%s " % (i, e) for i, e in enumerate(self.edges)]) + "\n"


if __name__ == "__main__":
    pass