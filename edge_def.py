import sys

class Edge:
    def __init__(self, inn, outn):
        self.inn = inn
        self.outn = outn
        self.label = self.get_label()
        
    def get_label(self):
        return self.outn.label[-1]
    
    def __repr__(self):
        return "%s -> %s = (%s)\n" % (self.inn, self.outn, self.label)
    
    def __eq__(self, other):
        return self.label == other.label and self.inn == other.inn and self.outn == other.outn
    
    def copy(self):
        return Edge(self.inn.copy(), self.outn.copy())

if __name__ == "__main__":
    pass