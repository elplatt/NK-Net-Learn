from elp_networks.network import *

class NestedClique(Network):
    
    _N = [1, 2, 6, 42, 1806]
    
    def __init__(self, m):
        '''Create an m-dimensional nested clique.'''
        self.m = m
        # Calculate up to N[m] if necessary
        for i in range(len(NestedClique._N), m+1):
            NestedClique._N.append(
                NestedClique._N[i-1]
                * (NestedClique._N[i-1] + 1))
    
    def nodes(self):
        '''Returns an iterator of nodes in the graph.'''
        N = NestedClique._N[self.m]
        for z in xrange(N):
            yield self._z2v(z)       
    
    def neighbors(self, v):
        '''Returns an iterator of the neighbors of a given node.'''
        # See paper notebook ELP-UM-001 p.51
        if len(v) != self.m:
            raise ValueError
        m = self.m
        z = self._v2z(v)
        w = list(v)
        zz = 0
        # Create level-k edges by changing lowest k values
        for i in xrange(m):
            Ni = NestedClique._N[i]
            if z % 2 == 1:
                w[i] = (w[i] - 1 - zz) % (Ni + 1)
                zz += Ni * v[i]
            else:
                w[i] = (w[i] + 1 + zz ) % (Ni + 1)
                zz += Ni * w[i]
            yield tuple(w)
    
    def _v2z(self, v):
        '''Convert from vertex to integer.'''
        z = 0
        for (i, vi) in enumerate(v):
            z += self._N[i] * vi
        return z
    
    def _z2v(self, z):
        '''Convert from integer to vertex.'''
        i = 0
        v = []
        zz = z
        while zz > 0 or i < self.m:
            N = self._N[i]
            nextN = self._N[i + 1]
            remainder = zz % nextN
            zz -= remainder
            v.append(int(remainder/N))
            i += 1
        return tuple(v)

    def path_length_histogram(self):
        surface = set([tuple([0] * self.m)])
        last_surface = set([])
        dist = []
        count = []
        surface_dist = 0
        while len(surface) > 0:
            dist.append(surface_dist)
            count.append(len(surface))
            next_surface = set()
            for v in surface:
                for w in self.neighbors(v):
                    if (w not in last_surface
                            and w not in surface):
                        next_surface.add(w)
            last_surface = surface
            surface = next_surface
            surface_dist += 1
        return (dist, count)
        
