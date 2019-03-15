import unittest
from elp_networks.algorithms.bfs import get_distances_bfs

no_edges = {0:set()}
tree_edges = {0:set([1,2]),1:set([3,4]),2:set([5,6])}
disjoint_edges = {
    0:set([1,2]),1:set([0,2]),2:set([0,1]),3:set([4,5]),4:set([3,5]),5:set([3,4])
}

class TestBFS(unittest.TestCase):

    def test_base(self):
        distances = get_distances_bfs(no_edges,0)
        self.assertEqual(distances,{0:0})

    def test_tree_root(self):
        distances = get_distances_bfs(tree_edges,0)
        self.assertEqual(distances,{0:0,1:1,2:1,3:2,4:2,5:2,6:2})

    def test_tree_mid(self):
        distances = get_distances_bfs(tree_edges,2)
        self.assertEqual(distances,{2:0,5:1,6:1})

    def test_disjoint_left(self):
        distances = get_distances_bfs(disjoint_edges,0)
        self.assertEqual(distances,{0:0,1:1,2:1})

    def test_disjoint_right(self):
        distances = get_distances_bfs(disjoint_edges,3)
        self.assertEqual(distances,{3:0,4:1,5:1})

if __name__ == '__main__':
    unittest.main()
    