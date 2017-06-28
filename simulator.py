import random

class Simulator(object):
    
    def __init__(self, model, edges):
        self.model = model
        self.edges = edges
        self.nodes = sorted(edges.keys())
        self.values = []
    
    def run(self, steps):
        self.init_state()
        next_state = {}
        for i in range(steps):
            step_total = 0
            for n in self.nodes:
                current_value = self.model.get_value(self.state[n])
                step_total += current_value
                next_node_state = self.state[n]
                next_value = current_value
                for neighbor in self.edges[n]:
                    new_value = self.model.get_value(self.state[neighbor])
                    if new_value > next_value:
                        next_value = new_value
                        next_node_state = self.state[neighbor]
                next_state[n] = next_node_state
            self.state = next_state
            self.values.append(step_total)
            
    def init_state(self):
        self.state = {}
        for n in self.nodes:
            self.state[n] = [random.getrandbits(1) for i in range(self.model.N)]