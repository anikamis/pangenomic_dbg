import sys

class Node:
    def __init__(self, label):
        self.label = label

        self.incoming = dict()
        self.outgoing = dict()

        self.strains = set()
        self.color = ""

    def copy_in(self):
        other = Node(self.label)
        other.incoming = self.incoming.copy()

        other.strains = self.strains.copy()
        other.color = self.color
        return other

    def copy_out(self):
        other = Node(self.label)

        other.outgoing = self.outgoing.copy()
        other.strains = self.strains.copy()
        other.color = self.color
        return other

    def copy(self):
        other = Node(self.label)

        other.incoming = self.incoming.copy()
        other.outgoing = self.outgoing.copy()
        other.strains = self.strains.copy()
        other.color = self.color
        return other
        
    def __repr__(self):
        return "(%s)" % self.label

    
    # co-lex order
    def __gt__(self, other):
        return self.label[::-1] > other.label[::-1]
    
    def __eq__(self, other):
        return self.label == other.label

    def colex(self):
        return self.label[::-1]
    
    def __hash__(self):
        return hash(self.label)
    
    def is_branching(self):
        return not (len(self.incoming) == 1 and len(self.outgoing) == 1)
    
    def add_strains(self, strains):
            self.strains.update(strains)


if __name__ == "__main__":
    pass