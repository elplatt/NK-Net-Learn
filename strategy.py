import random
import net

class Strategy(object):
    
    def get_next(self, states, edges):
        return states, edges

class BestNeighbor(Strategy):
    
    def __init__(self, model, edges, sample=0):
        self.model = model
        self.edges = edges
        self.sample = sample
        self.node_count = len(edges.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = list(states)
        new_values = list(values)
        for n in self.nodes:
            current_value = values[n]
            next_node_state = states[n]
            next_value = current_value
            if self.sample == 0:
                to_sample = self.edges[n]
            else:
                to_sample = random.sample(self.edges[n], self.sample)
            for neighbor in to_sample:
                new_value = self.model.get_value(states[neighbor])
                if new_value > next_value:
                    next_value = new_value
                    next_node_state = states[neighbor]
            new_states[n] = next_node_state
            new_values[n] = next_value
        return new_states, new_values

class Individual(Strategy):
    
    def __init__(self, model, edges):
        self.model = model
        self.edges = edges
        self.node_count = len(edges.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = []
        new_values = []
        N = self.model.N
        loci = range(N)
        trial_states, trial_values = self.model.get_hillclimb_values(states)
        current_values = values
        for n in self.nodes:
            next_value = current_values[n]
            next_node_state = states[n]
            for i in loci:
                new_value = trial_values[n*N + i]
                if new_value > next_value:
                    next_value = new_value
                    next_node_state = trial_states[n*N + i]
            new_states.append(next_node_state)
            new_values.append(next_value)
        return new_states, new_values

class BestNeighborIndividual(Strategy):
    
    def __init__(self, model, edges, sample=0):
        self.model = model
        self.edges = edges
        self.best = BestNeighbor(model, edges, sample)
        self.ind = Individual(model, edges)
        self.node_count = len(edges.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = list(states)
        new_values = list(values)
        next_best, best_values = self.best.get_next(states, values)
        next_ind, ind_values = self.ind.get_next(states, values)
        for n in self.nodes:
            value_best = best_values[n]
            value_ind = ind_values[n]
            if value_ind > value_best:
                new_states[n] = next_ind[n]
                new_values[n] = value_ind
            else:
                new_states[n] = next_best[n]
                new_values[n] = value_best
        return new_states, new_values

class Conformity(Strategy):
    
    def __init__(self, model, edges, sample=0):
        self.model = model
        self.edges = edges
        self.sample = sample
        self.node_count = len(edges.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = []
        for n in self.nodes:
            state_counts = {}
            if self.sample == 0:
                to_sample = self.edges[n]
            else:
                to_sample = random.sample(self.edges[n], self.sample)
            for neighbor in to_sample:
                try:
                    try:
                        state_counts[tuple(states[neighbor])] += 1
                    except TypeError:
                        print states[neighbor]
                        raise
                except KeyError:
                    state_counts[tuple(states[neighbor])] = 1
            max_counts = max([x[1] for x in state_counts.iteritems()])
            max_states = [list(x[0]) for x in state_counts.iteritems() if x[1] == max_counts]
            next_node_state = random.choice(max_states)
            new_states.append(next_node_state)
        new_values = self.model.get_values(new_states)
        return new_states, new_values

class ConformityIndividual(Strategy):
    
    def __init__(self, model, edges, sample=0):
        self.model = model
        self.edges = edges
        self.conform = Conformity(model, edges, sample)
        self.ind = Individual(model, edges)
        self.node_count = len(edges.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = []
        new_values = []
        next_conform, next_conform_values = self.conform.get_next(states, values)
        next_ind, next_ind_values = self.ind.get_next(states, values)
        for n in self.nodes:
            if next_ind_values[n] > next_conform_values[n]:
                new_states.append(next_ind[n])
                new_values.append(next_ind_values[n])
            else:
                new_states.append(next_conform[n])
                new_values.append(next_conform_values[n])
        return new_states, new_values

class LocalIndividual(Strategy):
    
    def __init__(self, model, edges_node_loc):
        self.model = model
        self.edges_node_loc = edges_node_loc
        self.node_by_loc = {}
        self.loc_by_node = {}
        for edge in edges_node_loc:
            node, loc = edge
            try:
                self.node_by_loc[loc].append(node)
            except KeyError:
                self.node_by_loc[loc] = [node]
            try:
                self.loc_by_node[node].append(loc)
            except KeyError:
                self.loc_by_node[node] = [loc]
        self.node_count = len(self.loc_by_node.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = list(states)
        new_values = list(values)
        N = self.model.N
        K = self.model.K
        loci = range(N)
        trial_states = []
        for n, state in enumerate(states):
            for loc in self.loc_by_node[n]:
                new_state = list(state)
                new_state[loc] = 1 - new_state[loc]
                trial_states.append(new_state)
        trial_values = self.model.get_values(trial_states)
        for n in self.nodes:
            current_value = values[n]
            next_state = states[n]
            next_value = current_value
            for i in range(K+1):
                new_value = trial_values[(K+1)*n + i]
                if new_value > next_value:
                    next_state = trial_states[(K+1)*n + i]
                    next_value = new_value
            new_states[n] = next_state
            new_values[n] = next_value
        return new_states, new_values

class LocalConformityIndividual(Strategy):
    
    def __init__(self, model, edges_node_loc, sample=0):
        self.model = model
        self.edges = net.affiliation_to_node(edges_node_loc)
        self.conform = Conformity(model, self.edges, sample)
        self.loc_ind = LocalIndividual(model, edges_node_loc)
        self.node_count = len(self.edges.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = list(states)
        new_values = list(values)
        next_conform, conform_values = self.conform.get_next(states, values)
        next_ind, ind_values = self.loc_ind.get_next(states, values)
        for n in range(self.node_count):
            value_conform = conform_values[n]
            value_ind = ind_values[n]
            if value_ind > value_conform:
                new_states[n] = next_ind[n]
                new_values[n] = value_ind
            else:
                new_states[n] = next_conform[n]
                new_values[n] = value_conform
        return new_states, new_values

class LocalBestNeighborIndividual(Strategy):
    
    def __init__(self, model, edges_node_loc, sample=0):
        self.model = model
        self.edges = net.affiliation_to_node(edges_node_loc)
        self.best = BestNeighbor(model, self.edges, sample)
        self.loc_ind = LocalIndividual(model, edges_node_loc)
        self.node_count = len(self.edges.keys())
        self.nodes = range(self.node_count)
        
    def get_next(self, states, values):
        new_states = list(states)
        new_values = list(values)
        next_best, best_values = self.best.get_next(states, values)
        next_ind, ind_values = self.loc_ind.get_next(states, values)
        for n in range(self.node_count):
            value_best = best_values[n]
            value_ind = ind_values[n]
            if value_ind > value_best:
                new_states[n] = next_ind[n]
                new_values[n] = value_ind
            else:
                new_states[n] = next_best[n]
                new_values[n] = value_best
        return new_states, new_values

class LocalIndividualConsensus(Strategy):
    
    def __init__(self, model, edges_node_loc, sample=0):
        self.model = model
        self.sample = sample
        self.node_by_loc = {}
        self.loc_by_node = {}
        for edge in edges_node_loc:
            node, loc = edge
            try:
                self.node_by_loc[loc].append(node)
            except KeyError:
                self.node_by_loc[loc] = [node]
            try:
                self.loc_by_node[node].append(loc)
            except KeyError:
                self.loc_by_node[node] = [loc]
        self.node_count = len(self.loc_by_node.keys())
        self.nodes = range(self.node_count)
    
    def get_next(self, states, values):
        best_states = []
        state = states[0]
        state_value = values[0]
        N = self.model.N
        K = self.model.K
        loci = range(N)
        # Hill climbing for connected subset of NK cells
        trial_states = []
        for n in range(self.node_count):
            for loc in self.loc_by_node[n]:
                new_state = list(state)
                new_state[loc] = 1 - new_state[loc]
                trial_states.append(new_state)
        trial_values = self.model.get_values(trial_states)
        for n in range(self.node_count):
            next_state = list(state)
            next_value = state_value
            for i in range(K+1):
                new_value = trial_values[(K+1)*n + i]
                if new_value > next_value:
                    next_value = new_value
                    next_state = trial_states[(K+1)*n + i]
            best_states.append(next_state)
        # Local (per-NK-cell) Consensus
        loc_total = [0] * self.model.N
        loc_count = [0] * self.model.N
        for node, locs in self.loc_by_node.iteritems():
            for l in locs:
                loc_count[l] += 1
                loc_total[l] += best_states[node][l]
        next_state = list(state)
        # Majority vote
        for l in range(self.model.N):
            if float(loc_total[l]) / float(loc_count[l]) == 0.5:
                continue
            if float(loc_total[l]) / float(loc_count[l]) > 0.5:
                next_state[l] = 1
            else:
                next_state[l] = 0
        next_value = self.model.get_value(next_state)
        return [next_state] * len(states), [next_value] * len(states)
        
