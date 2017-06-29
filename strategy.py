import random

class Strategy(object):
    
    def get_next(model, edges, state):
        return state

class BestNeighbor(Strategy):
    
    def __init__(self, model, edges):
        self.model = model
        self.edges = edges
        
    def get_next(self, states, n):
        current_value = self.model.get_value(states[n])
        next_node_state = states[n]
        next_value = current_value
        for neighbor in self.edges[n]:
            new_value = self.model.get_value(states[neighbor])
            if new_value > next_value:
                next_value = new_value
                next_node_state = states[neighbor]
        return next_node_state

class Individual(Strategy):
    
    def __init__(self, model, edges):
        self.model = model
        self.edges = edges
        
    def get_next(self, states, n):
        current_value = self.model.get_value(states[n])
        next_node_state = states[n]
        next_value = current_value
        for i in range(len(states[n])):
            new_state = list(states[n])
            new_state[i] = 1 - new_state[i]
            new_value = self.model.get_value(new_state)
            if new_value > next_value:
                next_value = new_value
                next_node_state = new_state
        return next_node_state

class BestNeighborIndividual(Strategy):
    
    def __init__(self, model, edges):
        self.model = model
        self.edges = edges
        self.best = BestNeighbor(model, edges)
        self.ind = Individual(model, edges)
        
    def get_next(self, states, n):
        next_best = self.best.get_next(states, n)
        value_best = self.model.get_value(next_best)
        next_ind = self.ind.get_next(states, n)
        value_ind = self.model.get_value(next_ind)
        if value_ind > value_best:
            return next_ind
        return next_best

class Conformity(Strategy):
    
    def __init__(self, model, edges):
        self.model = model
        self.edges = edges
        
    def get_next(self, states, n):
        state_counts = {}
        for neighbor in self.edges[n]:
            try:
                state_counts[tuple(states[neighbor])] += 1
            except KeyError:
                state_counts[tuple(states[neighbor])] = 1
        max_counts = max([x[1] for x in state_counts.iteritems()])
        max_states = [list(x[0]) for x in state_counts.iteritems() if x[1] == max_counts]
        next_node_state = random.choice(max_states)
        return next_node_state

class ConformityIndividual(Strategy):
    
    def __init__(self, model, edges):
        self.model = model
        self.edges = edges
        self.conform = Conformity(model, edges)
        self.ind = Individual(model, edges)
        
    def get_next(self, states, n):
        next_conform = self.conform.get_next(states, n)
        value_conform = self.model.get_value(next_conform)
        next_ind = self.ind.get_next(states, n)
        value_ind = self.model.get_value(next_ind)
        if value_ind > value_conform:
            return next_ind
        return next_conform


