import math
from network import *

class Lattice(Network):
    """Generalized lattice."""
    
    def __init__(self, m, L):
        '''Create an m-dimensional grid with length L.'''
        self.m = m
        self.L = L
    
    def nodes(self):
        dimension = self.m
        current = [0] * self.m
        while True:
            if dimension == self.m:
                # All dimensions updated, yield new node
                yield tuple(current)
                dimension -= 1
            else:
                # Update current dimension
                current[dimension] += 1
                if current[dimension] == self.L:
                    # Reset this dimension and move back one
                    current[dimension] = 0
                    dimension -= 1
                    if dimension < 0:
                        # All combinations have been yielded
                        break
                else:
                    # Move all the way to the right
                    dimension = self.m
    
    def neighbors(self, v):
        for i in xrange(self.m):
            w = list(v)
            w[i] = (v[i] + 1) % self.L
            yield tuple(w)
            w[i] = (v[i] - 1) % self.L
            yield tuple(w)
            

