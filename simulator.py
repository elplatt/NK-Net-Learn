import random
import strategy

class Simulator(object):
    
    def __init__(self, model, edges, strat=None):
        self.model = model
        self.edges = edges
        self.nodes = sorted(edges.keys())
        self.values = []
        if strat is None:
            self.strategy = strategy.BestNeighbor(model, edges)
        else:
            self.strategy = strat
    
    def run(self, steps):
        self.init_state()
        next_state = {}
        for i in range(steps):
            step_total = 0
            for n in self.nodes:
                current_value = self.model.get_value(self.state[n])
                step_total += current_value
                next_state[n] = self.strategy.get_next(self.state, n)
            self.state = next_state
            self.values.append(step_total / float(len(self.nodes)))
            
    def init_state(self):
        self.state = {}
        for n in self.nodes:
            self.state[n] = [random.getrandbits(1) for i in range(self.model.N)]