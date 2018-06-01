import elp_networks as enet
import unittest

square_nodes = set(range(4)) 
square_edges = set([
    frozenset((0,1)), frozenset((1,3)), frozenset((3,2)), frozenset((2,0))
])
square_neighbors = {
    0: frozenset((1,2)),
    1: frozenset((0,3)),
    2: frozenset((0,3)),
    3: frozenset((1,2)),
}

butterfly_nodes = set([
    (0, 0)
    , (0, 1)
    , (0, 2)
    , (0, 3)
    , (1, 0)
    , (1, 1)
    , (1, 2)
    , (1, 3)
])
butterfly_edges = set([
    frozenset(((0, 0), (1, 0)))
    , frozenset(((0, 0), (1, 1)))
    , frozenset(((0, 1), (1, 0)))
    , frozenset(((0, 1), (1, 1)))
    , frozenset(((0, 2), (1, 2)))
    , frozenset(((0, 2), (1, 3)))
    , frozenset(((0, 3), (1, 2)))
    , frozenset(((0, 3), (1, 3)))
    , frozenset(((0, 3), (1, 1)))
    , frozenset(((0, 1), (1, 3)))
    , frozenset(((0, 0), (1, 2)))
    , frozenset(((0, 2), (1, 0)))
])
butterfly_neighbors = {
    (0, 0): frozenset([(1,0),(1,1),(1,2)])
    , (0, 1): frozenset([(1,1),(1,0),(1,3)])
    , (0, 2): frozenset([(1,2),(1,3),(1,0)])
    , (0, 3): frozenset([(1,3),(1,2),(1,1)])
    , (1, 0): frozenset([(0,0),(0,2),(0,1)])
    , (1, 1): frozenset([(0,1),(0,3),(0,0)])
    , (1, 2): frozenset([(0,2),(0,0),(0,3)])
    , (1, 3): frozenset([(0,3),(0,1),(0,2)])  
}

nq_two_nodes = set([ (0,0), (1,0), (0,1), (1,1), (0,2), (1,2) ])
nq_two_edges = set([
    frozenset([ (0,0), (1,2) ])
    , frozenset([ (0,0), (1,0) ])
    , frozenset([ (0,1), (1,0) ])
    , frozenset([ (0,1), (1,1) ])
    , frozenset([ (0,2), (1,1) ])
    , frozenset([ (0,2), (1,2) ])    
])
nq_two_neighbors = {
    (0,0): frozenset([(1,2), (1,0)])
    , (1,0): frozenset([(0,1),(0,0)])
    , (0,1): frozenset([(1,0),(1,1)])
    , (1,1): frozenset([(0,2),(0,1)])
    , (0,2): frozenset([(1,1),(1,2)])
    , (1,2): frozenset([(0,0),(0,2)])
}

nq_three_nodes = set([
    (0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,2,0), (1,2,0)
    ,(0,0,1), (1,0,1), (0,1,1), (1,1,1), (0,2,1), (1,2,1)
    ,(0,0,2), (1,0,2), (0,1,2), (1,1,2), (0,2,2), (1,2,2)
    ,(0,0,3), (1,0,3), (0,1,3), (1,1,3), (0,2,3), (1,2,3)
    ,(0,0,4), (1,0,4), (0,1,4), (1,1,4), (0,2,4), (1,2,4)
    ,(0,0,5), (1,0,5), (0,1,5), (1,1,5), (0,2,5), (1,2,5)
    ,(0,0,6), (1,0,6), (0,1,6), (1,1,6), (0,2,6), (1,2,6)
])

nq_three_neighbors = {
    (0,0,0): frozenset([(1,2,6),(1,2,0),(1,0,0)])
    , (1,0,0): frozenset([(0,1,5),(0,1,0),(0,0,0)])
    , (0,1,0): frozenset([(1,0,2),(1,0,0),(1,1,0)])
    , (1,1,0): frozenset([(0,2,3),(0,2,0),(0,1,0)])
    , (0,2,0): frozenset([(1,1,4),(1,1,0),(1,2,0)])
    , (1,2,0): frozenset([(0,0,1),(0,0,0),(0,2,0)])
    , (0,0,1): frozenset([(1,2,0),(1,2,1),(1,0,1)])
    , (1,0,1): frozenset([(0,1,6),(0,1,1),(0,0,1)])
    , (0,1,1): frozenset([(1,0,3),(1,0,1),(1,1,1)])
    , (1,1,1): frozenset([(0,2,4),(0,2,1),(0,1,1)])
    , (0,2,1): frozenset([(1,1,5),(1,1,1),(1,2,1)])
    , (1,2,1): frozenset([(0,0,2),(0,0,1),(0,2,1)])
    , (0,0,2): frozenset([(1,2,1),(1,2,2),(1,0,2)])
    , (1,0,2): frozenset([(0,1,0),(0,1,2),(0,0,2)])
    , (0,1,2): frozenset([(1,0,4),(1,0,2),(1,1,2)])
    , (1,1,2): frozenset([(0,2,5),(0,2,2),(0,1,2)])
    , (0,2,2): frozenset([(1,1,6),(1,1,2),(1,2,2)])
    , (1,2,2): frozenset([(0,0,3),(0,0,2),(0,2,2)])
    , (0,0,3): frozenset([(1,2,2),(1,2,3),(1,0,3)])
    , (1,0,3): frozenset([(0,1,1),(0,1,3),(0,0,3)])
    , (0,1,3): frozenset([(1,0,5),(1,0,3),(1,1,3)])
    , (1,1,3): frozenset([(0,2,6),(0,2,3),(0,1,3)])
    , (0,2,3): frozenset([(1,1,0),(1,1,3),(1,2,3)])
    , (1,2,3): frozenset([(0,0,4),(0,0,3),(0,2,3)])
    , (0,0,4): frozenset([(1,2,3),(1,2,4),(1,0,4)])
    , (1,0,4): frozenset([(0,1,2),(0,1,4),(0,0,4)])
    , (0,1,4): frozenset([(1,0,6),(1,0,4),(1,1,4)])
    , (1,1,4): frozenset([(0,2,0),(0,2,4),(0,1,4)])
    , (0,2,4): frozenset([(1,1,1),(1,1,4),(1,2,4)])
    , (1,2,4): frozenset([(0,0,5),(0,0,4),(0,2,4)])
    , (0,0,5): frozenset([(1,2,4),(1,2,5),(1,0,5)])
    , (1,0,5): frozenset([(0,1,3),(0,1,5),(0,0,5)])
    , (0,1,5): frozenset([(1,0,0),(1,0,5),(1,1,5)])
    , (1,1,5): frozenset([(0,2,1),(0,2,5),(0,1,5)])
    , (0,2,5): frozenset([(1,1,2),(1,1,5),(1,2,5)])
    , (1,2,5): frozenset([(0,0,6),(0,0,5),(0,2,5)])
    , (0,0,6): frozenset([(1,2,5),(1,2,6),(1,0,6)])
    , (1,0,6): frozenset([(0,1,4),(0,1,6),(0,0,6)])
    , (0,1,6): frozenset([(1,0,1),(1,0,6),(1,1,6)])
    , (1,1,6): frozenset([(0,2,2),(0,2,6),(0,1,6)])
    , (0,2,6): frozenset([(1,1,3),(1,1,6),(1,2,6)])
    , (1,2,6): frozenset([(0,0,0),(0,0,6),(0,2,6)])
}

nq_three_edges = set([
    frozenset([ (0,0,0), (1,0,0) ])
    , frozenset([ (1,0,0), (0,1,0) ])
    , frozenset([ (0,1,0), (1,1,0) ])
    , frozenset([ (1,1,0), (0,2,0) ])
    , frozenset([ (0,2,0), (1,2,0) ])
    , frozenset([ (1,2,0), (0,0,0) ])
    , frozenset([ (0,0,1), (1,0,1) ])
    , frozenset([ (1,0,1), (0,1,1) ])
    , frozenset([ (0,1,1), (1,1,1) ])
    , frozenset([ (1,1,1), (0,2,1) ])
    , frozenset([ (0,2,1), (1,2,1) ])
    , frozenset([ (1,2,1), (0,0,1) ])
    , frozenset([ (0,0,2), (1,0,2) ])
    , frozenset([ (1,0,2), (0,1,2) ])
    , frozenset([ (0,1,2), (1,1,2) ])
    , frozenset([ (1,1,2), (0,2,2) ])
    , frozenset([ (0,2,2), (1,2,2) ])
    , frozenset([ (1,2,2), (0,0,2) ])
    , frozenset([ (0,0,3), (1,0,3) ])
    , frozenset([ (1,0,3), (0,1,3) ])
    , frozenset([ (0,1,3), (1,1,3) ])
    , frozenset([ (1,1,3), (0,2,3) ])
    , frozenset([ (0,2,3), (1,2,3) ])
    , frozenset([ (1,2,3), (0,0,3) ])
    , frozenset([ (0,0,4), (1,0,4) ])
    , frozenset([ (1,0,4), (0,1,4) ])
    , frozenset([ (0,1,4), (1,1,4) ])
    , frozenset([ (1,1,4), (0,2,4) ])
    , frozenset([ (0,2,4), (1,2,4) ])
    , frozenset([ (1,2,4), (0,0,4) ])
    , frozenset([ (0,0,5), (1,0,5) ])
    , frozenset([ (1,0,5), (0,1,5) ])
    , frozenset([ (0,1,5), (1,1,5) ])
    , frozenset([ (1,1,5), (0,2,5) ])
    , frozenset([ (0,2,5), (1,2,5) ])
    , frozenset([ (1,2,5), (0,0,5) ])
    , frozenset([ (0,0,6), (1,0,6) ])
    , frozenset([ (1,0,6), (0,1,6) ])
    , frozenset([ (0,1,6), (1,1,6) ])
    , frozenset([ (1,1,6), (0,2,6) ])
    , frozenset([ (0,2,6), (1,2,6) ])
    , frozenset([ (1,2,6), (0,0,6) ])
    , frozenset([ (1,0,0), (0,1,5) ])
    , frozenset([ (1,1,0), (0,2,3) ])
    , frozenset([ (1,2,0), (0,0,1) ])
    , frozenset([ (1,0,1), (0,1,6) ])
    , frozenset([ (1,1,1), (0,2,4) ])
    , frozenset([ (1,2,1), (0,0,2) ])
    , frozenset([ (1,0,2), (0,1,0) ])
    , frozenset([ (1,1,2), (0,2,5) ])
    , frozenset([ (1,2,2), (0,0,3) ])
    , frozenset([ (1,0,3), (0,1,1) ])
    , frozenset([ (1,1,3), (0,2,6) ])
    , frozenset([ (1,2,3), (0,0,4) ])
    , frozenset([ (1,0,4), (0,1,2) ])
    , frozenset([ (1,1,4), (0,2,0) ])
    , frozenset([ (1,2,4), (0,0,5) ])
    , frozenset([ (1,0,5), (0,1,3) ])
    , frozenset([ (1,1,5), (0,2,1) ])
    , frozenset([ (1,2,5), (0,0,6) ])
    , frozenset([ (1,0,6), (0,1,4) ])
    , frozenset([ (1,1,6), (0,2,2) ])
    , frozenset([ (1,2,6), (0,0,0) ])
])

class TestCube(unittest.TestCase):
    
    def test_base(self):
        cube = enet.Cube(0)
        self.assertEqual(set(cube.nodes()), set((0,)))
        
    def test_square_nodes(self):
        cube = enet.Cube(2)
        self.assertEqual(set(cube.nodes()), square_nodes)

    def test_square_neighbors(self):
        cube = enet.Cube(2)
        for v in square_nodes:
            self.assertEqual(set(cube.neighbors(v)), square_neighbors[v])

class TestButterfly(unittest.TestCase):
    
    def test_one(self):
        net = enet.Butterfly(1)
        self.assertEqual(set(net.nodes()), set([(0,0), (0,1)]))
        self.assertEqual(set(net.neighbors((0,0))), set([(0,1)]))
        self.assertEqual(set(net.neighbors((0,1))), set([(0,0)]))

    def test_two(self):
        net = enet.Butterfly(2)
        self.assertEqual(set(net.nodes()), butterfly_nodes)
        for v, neighbors in butterfly_neighbors.items():
            self.assertEqual(set(net.neighbors(v)), neighbors)

class TestNestedClique(unittest.TestCase):
    
    def test_N(self):
        net = enet.NestedClique(5)
        self.assertEqual(enet.NestedClique._N[5], 1806*1807)
    
    def test_z2v(self):
        net = enet.NestedClique(3)
        z = 0*1 + 2*2 + 3*6
        self.assertEqual(net._z2v(z), (0, 2, 3))
        
    def test_v2z(self):
        net = enet.NestedClique(3)
        v = (0, 2, 3)
        z =  0*1 + 2*2 + 3*6
        self.assertEqual(net._v2z(v), z)
    
    def test_base(self):
        net = enet.NestedClique(0)
        self.assertEqual(set(net.nodes()), set([()]))
        self.assertEqual(set(net.neighbors(())), set())
        
    def test_one(self):
        net = enet.NestedClique(1)
        self.assertEqual(set(net.nodes()), set([(0,), (1,)]))
        self.assertEqual(set(net.neighbors((0,))), set([(1,)]))
        self.assertEqual(set(net.neighbors((1,))), set([(0,)]))
        
    def test_two(self):
        net = enet.NestedClique(2)
        self.assertEqual(set(net.nodes()), nq_two_nodes)
        for v, neighbors in nq_two_neighbors.items():
            self.assertEqual(set(net.neighbors(v)), neighbors)

    def test_three(self):
        net = enet.NestedClique(3)
        self.assertEqual(set(net.nodes()), nq_three_nodes)
        for v, neighbors in nq_three_neighbors.items():
            self.assertEqual(set(net.neighbors(v)), neighbors)

class TestLattice(unittest.TestCase):
    
    def test_one(self):
        net = enet.Lattice(1, 3)
        self.assertEqual(set(net.nodes()), set([(0,),(1,),(2,)]))
        self.assertEqual(set(net.neighbors((0,))), set([(1,), (2,)]))
        
    def test_two(self):
        net = enet.Lattice(2, 3)
        self.assertEqual(
            set(net.nodes()),
            set([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]))
        self.assertEqual(
            set(net.neighbors((0,1))),
            set([(2,1),(1,1),(0,0),(0,2)])
        )

if __name__ == '__main__':
    unittest.main()
    