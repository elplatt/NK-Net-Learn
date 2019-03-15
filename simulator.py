import random
import strategy

class Simulator(object):
    
    def __init__(self, model, nodes, edges, strat=None):
        self.model = model
        self.edges = edges
        self.nodes = nodes
        self.node_count = len(self.nodes)
        self.values = []
        self.mean_values = []
        self.states = []
        self.state = {}
        if strat is None:
            self.strategy = strategy.BestNeighbor(model, edges)
        else:
            self.strategy = strat
    
    def run(self, steps):
        self.init_state()
        self.states.append(self.state)
        next_values = self.model.get_values(self.state)
        self.values.append(next_values)
        self.mean_values.append(sum(next_values.values()) / float(len(self.nodes)))
        for i in range(steps):
            next_state, next_values = self.strategy.get_next(self.state, next_values)
            self.state = next_state
            self.states.append(self.state)
            self.values.append(next_values)
            self.mean_values.append(sum(next_values.values()) / float(len(self.nodes)))
            
    def init_state(self):
        self.state = dict([
            (j, 
            [random.getrandbits(1) for i in range(self.model.N)])
            for j in self.nodes])
