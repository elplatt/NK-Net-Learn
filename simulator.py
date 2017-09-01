import random
import strategy

class Simulator(object):
    
    def __init__(self, model, nodes, edges, strat=None):
        self.model = model
        self.edges = edges
        self.nodes = nodes
        self.node_count = len(self.nodes)
        self.values = []
        if strat is None:
            self.strategy = strategy.BestNeighbor(model, edges)
        else:
            self.strategy = strat
    
    def run(self, steps):
        self.init_state()
        next_values = self.model.get_values(self.states)
        self.values.append(sum(next_values) / float(len(self.nodes)))
        for i in range(steps):
            next_states, next_values = self.strategy.get_next(self.states, next_values)
            self.states = next_states
            self.values.append(sum(next_values) / float(len(self.nodes)))
            
    def init_state(self):
        self.states = dict([
            (j, 
            [random.getrandbits(1) for i in range(self.model.N)])
            for j in self.nodes])
