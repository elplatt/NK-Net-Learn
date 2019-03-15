import math
from elp_networks.network import *

class Cube(Network):
    """Generalized cube network."""
    
    def __init__(self, m):
        '''Create an m-dimensional cube.'''
        self.m = m
    
    def nodes(self):
        return xrange(pow(2,self.m))
    
    def neighbors(self, v):
        for i in xrange(self.m):
            yield v ^ (1 << i)
    
    def pathlength_counts(self):
        m = self.m
        lengths = range(m + 1)
        counts = [math.factorial(m) / math.factorial(h) / math.factorial(m-h) for h in lengths]
        return (lengths, counts)

