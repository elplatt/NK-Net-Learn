import unittest
from min_cut import (
    dinic_unit_pairwise,
    edmonds_karp_pairwise
)

edges_from = {
    1: [2,4,5],
    2: [],
    3: [2,4],
    4: [1,5],
    5: [4,6],
    6: [5]
}
# Calculations in ELP-UM-001, p103
true_mincuts = [
    (1,2,1),(1,3,0),(1,4,2),(1,5,2),(1,6,1),
    (2,1,0),(2,3,0),(2,4,0),(2,5,0),(2,6,0),
    (3,1,1),(3,2,2),(3,4,1),(3,5,1),(3,6,1),
    (4,1,1),(4,2,1),(4,3,0),(4,5,2),(4,6,1),
    (5,1,1),(5,2,1),(5,3,0),(5,4,1),(5,6,1),
    (6,1,1),(6,2,1),(6,3,0),(6,4,1),(6,5,1)]

class EdmondsKarpTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_return(self):
        mincuts = list(edmonds_karp_pairwise(edges_from))
        self.assertEqual(mincuts, true_mincuts)

class DinicUnitTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_return(self):
        mincuts = list(dinic_unit_pairwise(edges_from))
        self.assertEqual(mincuts, true_mincuts)

if __name__ == '__main__':
    unittest.main()
    