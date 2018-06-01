from network import *

class Ring(Network):
    
    def __init__(self, n, m=1):
        '''Create an n-node ring with connections to 2m nearest neighbors.'''
        self.m = m
        self.n = n
        # Create nodes
        self.nodes = set(range(0,n))
        # Create edges
        self.edges = set()
        for v in self.nodes:
            for delta in range(1,m+1):
                w = delta % n
                self.edges.add(frozenset((v, w)))
    
    def nodes(self):
        return xrange(n)
    
    def neighbors(self, v):
        for delta in xrange(1,self.m+1):
            yield (v - delta) % self.n
            yield (v + delta) % self.n
