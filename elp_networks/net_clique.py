from network import *

class Clique(Network):
    
    def __init__(self, m):
        '''Create an m-node clique.'''
        self.m = m
    
    def nodes(self):
        return xrange(self.m)
    
    def neighbors(self, v):
        for w in xrange(self.m):
            if w == v:
                continue
            yield w
