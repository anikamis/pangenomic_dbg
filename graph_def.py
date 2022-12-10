# from edge_def import Edge as E
# from node_def import Node as N

# class Graph:
#     def __init__(self, nodes=dict(), edges=list(E())):
#         self.nodes = nodes  # k-1 mers
#         self.edges = edges  # k mers

#         # G’s edges sorted co-lexicographically by their starting nodes, 
#         # with ties broken co-lexicographically by their ending nodes

#         # edges in E in colex order by their ending nodes, where ties are broken by their starting nodes
#         self.L = sorted(self.edges, key=lambda x: (x.inn.colex(), x.outn.colex()))

#         # edges in E sorted colex by their starting nodes, with ties broken by their ending nodes
#         self.F = sorted(self.edges, key=lambda x: (x.outn.colex(), x.inn.colex()))

#         # nodes sorted in colex order
#         self.colex_nodes = sorted(self.nodes.keys(), key = lambda x: x.colex())

#         # sequence of edge labels sorted according to the edges’ order in L
#         self.ebwt = [node[-1] for node in self.L]

#         # bitvector with a 1 marking the position in L of the last outgoing edge of each node
#         self.bL = ""
#         for nodes in self.colex_nodes:
#             position = self.L.find(nodes.outgoing[-1])
#             if position == -1:
#                 position == 0 # TODO: account for modification so all nodes except for starting node has incoming edges
#             self.bL += position * "0" + "1"

#         # build select list for each character in the ebwt, this makes finding rank faster!
#         alphabet = set(self.ebwt)
#         self.select_map = {c:[] for c in alphabet}
#         for i, c in enumerate(self.ebwt):
#             self.select_map[c].append(i)


#         # self.preceding_labels = {} # TODO: define map to hold preceding labels for all characters for faster getting of preceding colexes


#     def all_nodes(self):
#         return set([n.label for n in self.nodes])

    
#     ''' number of times label e appears in the ebwt up to but not including index p'''
#     def rank(self, e, p):
#         # take advantage of how we can find rank from select list instead of using a linear scan
#         for i, offset in enumerate(self.select_map(e)):
#             if offset > p:
#                 return i - 1
#         return len(self.select_map(e))

#     def get_colex_preceding(self, e):
#         return set([d for d in self.edges if d.label < e.label])

#     def pos_F_from_L(self, e, p):
#         return len(self.get_colex_preceding(self, e)) + self.rank(e, p) - 1

#     def bitvector_access(self, b, i):
#         return b[i]


#     # def __iadd__(self, obj):
#     #     if isinstance(obj, list):
#     #         if len(obj) and isinstance(obj, E):
#     #             self.edges += obj
#     #         elif len(obj) and isinstance(obj, N):
#     #             self.nodes += obj
#     #         else:
#     #             raise TypeError("Graph can only add lists of Edges or Nodes")
#     #     elif isinstance(obj, E):
#     #         self.edges += [obj]
#     #     elif isinstance(obj, N):
#     #         self.nodes += [obj]
#     #     else:
#     #         raise TypeError("Graph can only add Edges or Nodes")


#     def __repr__(self):
#         nums = "nodes: %s, edges: %s\n" % (len(self.nodes), len(self.edges))
#         return nums + "\n".join(["%d:\t%s " % (i, e) for i, e in enumerate(self.edges)]) + "\n"


# if __name__ == "__main__":
#     pass

from edge_def import Edge as E
from node_def import Node as N

class Graph:
    def __init__(self, nodes=dict(), edges=list()):
        self.nodes = nodes
        self.edges = edges

    def all_nodes(self):
        return set([n.label for n in self.nodes])

    # def __iadd__(self, obj):
    #     if isinstance(obj, list):
    #         if len(obj) and isinstance(obj, E):
    #             self.edges += obj
    #         elif len(obj) and isinstance(obj, N):
    #             self.nodes += obj
    #         else:
    #             raise TypeError("Graph can only add lists of Edges or Nodes")
    #     elif isinstance(obj, E):
    #         self.edges += [obj]
    #     elif isinstance(obj, N):
    #         self.nodes += [obj]
    #     else:
    #         raise TypeError("Graph can only add Edges or Nodes")


    def __repr__(self):
        nums = "nodes: %s, edges: %s\n" % (len(self.nodes), len(self.edges))
        return nums + "\n".join(["%d:\t%s " % (i, e) for i, e in enumerate(self.edges)]) + "\n"


if __name__ == "__main__":
    pass