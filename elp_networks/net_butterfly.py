import math
from elp_networks.network import *

class Butterfly(Network):
    
    def __init__(self, m):
        '''Create an m-dimensional butterfly network.'''
        self.m = m

    def nodes(self):
        in_level_max = pow(2, self.m)
        for level in xrange(self.m):
            for in_level in xrange(in_level_max):
                node = (level, in_level)
                yield node
        
    def int_nodes(self):
        for z, l in self.nodes():
            yield z*2**self.m + l
        
    def neighbors(self, v):
        sofar = set([v])
        level, in_level = v
        down = ((level + 1) % self.m, in_level)
        if down not in sofar:
            yield down
            sofar.add(down)
        down_right = ((level + 1) % self.m, in_level ^ (1 << level))
        if down_right not in sofar:
            yield down_right
            sofar.add(down_right)
        up = ((level - 1) % self.m, in_level)
        if up not in sofar:
            yield up
            sofar.add(up)
        up_left = ((level - 1) % self.m, in_level ^ (1 << ((level - 1) % self.m)))
        if up_left not in sofar:
            yield up_left
            sofar.add(up_left)

    def int_neighbors(self, vi):
        z = int(math.floor(vi / 2**self.m))
        l = vi - z * 2**self.m
        for nz, nl in self.neighbors((z,l)):
            yield nz*2**self.m + nl