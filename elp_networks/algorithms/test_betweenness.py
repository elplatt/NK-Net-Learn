import unittest
from betweenness import betweenness, recalculated_betweenness

weight_from_to = {
    ("A", "B"): 1,
    ("A", "C"): 2,
    ("B", "D"): 2,
    ("C", "D"): 1,
    ("D", "A"): 3,
    ("D", "C"): 1
}

true_dist = {
    'A': {'A':0, 'B':1, 'C':2, 'D':3},
    'B': {'A':5, 'B':0, 'C':3, 'D':2},
    'C': {'A':4, 'B':5, 'C':0, 'D':1},
    'D': {'A':3, 'B':4, 'C':1, 'D':0}
}

true_paths = {
    'A': {'A':[[]], 'B':[[]], 'C':[[]], 'D':[['B'],['C']]},
    'B': {'A':[['D']], 'B':[[]], 'C':[['D']], 'D':[[]]},
    'C': {'A':[['D']], 'B':[['D','A']], 'C':[[]], 'D':[[]]},
    'D': {'A':[[]], 'B':[['A']], 'C':[[]], 'D':[[]]}
}

true_betweenness = {'A':2, 'B':0.5, 'C':0.5, 'D':4}
true_betweenness_normalized = {'A':2.0/6.0, 'B':0.5/6.0, 'C':0.5/6.0, 'D':4.0/6.0}

recalc_weight_from_to = {
    ('A','B'): 1,
    ('A','C'): 1,
    ('A','D'): 1,
    ('B','A'): 1,
    ('C','A'): 1,
    ('D','A'): 1,
    ('B','C'): 3,
    ('B','D'): 3,
    ('C','B'): 3,
    ('D','B'): 3,
    ('D','C'): 7,
    ('C','D'): 7    
}
recalc_true_betweenness = [('A', 6.0), ('B', 2.0)]

class TestBetweenness(unittest.TestCase):
    
    def test_betweenness(self):
        b = betweenness(weight_from_to)
        self.assertEqual(b, true_betweenness_normalized)

    def test_betweenness_unnormalized(self):
        b = betweenness(weight_from_to, normalized=False)
        self.assertEqual(b, true_betweenness)

    def test_betweenness_recalculated(self):
        b = recalculated_betweenness(recalc_weight_from_to, normalized=False)
        self.assertEqual(list(b), recalc_true_betweenness)

if __name__ == '__main__':
    unittest.main()
    