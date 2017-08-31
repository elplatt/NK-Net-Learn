import random
import net

def edges_to_nodes(edges):
    nodes = set()
    for s, targets in edges.iteritems():
        nodes.add(s)
        nodes = nodes | set(targets)
    return nodes

def edges_node_loc_to_nodes(edges_node_loc):
    nodes = set()
    for node, loc in edges_node_loc:
        nodes.add(node)
    return nodes

class Strategy(object):
    
    def get_next(self, states, edges):
        return states, edges

class BestNeighbor(Strategy):
    
    def __init__(self, model, edges, sample=0):
        self.model = model
        self.edges = edges
        self.sample = sample
        self.nodes = edges_to_nodes(edges)
        self.node_count = len(self.nodes)
        
    def get_next(self, states, values):
        new_states = dict(states)
        new_values = dict(values)
        for n in self.nodes:
            current_value = values[n]
            next_node_state = states[n]
            next_value = current_value
            if self.sample == 0 or len(self.edges[n]) <= self.sample:
                to_sample = self.edges[n]
            else:
                to_sample = random.sample(self.edges[n], self.sample)
            for neighbor in to_sample:
                try:
                    new_value = self.model.get_value(states[neighbor])
                except IndexError:
                    print len(states)
                    print to_sample
                    print neighbor
                    raise
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
        self.nodes = edges_to_nodes(edges)
        self.node_count = len(self.nodes)
        
    def get_next(self, states, values):
        new_states = {}
        new_values = {}
        N = self.model.N
        loci = range(N)
        trial_states, trial_values = self.model.get_hillclimb_values(states)
        current_values = values
        for n in self.nodes:
            node_values = trial_values[n]
            node_states = trial_states[n]
            next_value = current_values[n]
            next_node_state = states[n]
            for i in loci:
                new_value = node_values[i]
                if new_value > next_value:
                    next_value = new_value
                    next_node_state = node_states[i]
            new_states[n] = next_node_state
            new_values[n] = next_value
        return new_states, new_values

class BestNeighborIndividual(Strategy):
    
    def __init__(self, model, edges, sample=0):
        self.model = model
        self.edges = edges
        self.best = BestNeighbor(model, edges, sample)
        self.ind = Individual(model, edges)
        self.nodes = edges_to_nodes(edges)
        self.node_count = len(self.nodes)
        
    def get_next(self, states, values):
        new_states = dict(states)
        new_values = dict(values)
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
        self.nodes = edges_to_nodes(edges)
        self.node_count = len(self.nodes)
        
    def get_next(self, states, values):
        new_states = {}
        for n in self.nodes:
            state_counts = {}
            if self.sample == 0 or len(self.edges[n]) <= self.sample:
                to_sample = self.edges[n]
            else:
                to_sample = random.sample(self.edges[n], self.sample)
            for neighbor in to_sample:
                try:
                    state_counts[tuple(states[neighbor])] += 1
                except KeyError:
                    state_counts[tuple(states[neighbor])] = 1
            if len(to_sample) == 0:
                next_node_state = states[n]
            else:
                max_counts = max([x[1] for x in state_counts.iteritems()])
                max_states = [list(x[0]) for x in state_counts.iteritems() if x[1] == max_counts]
                next_node_state = random.choice(max_states)
            new_states[n] = next_node_state
        new_values = self.model.get_values(new_states)
        return new_states, new_values

class ConformityIndividual(Strategy):
    
    def __init__(self, model, edges, sample=0):
        self.model = model
        self.edges = edges
        self.conform = Conformity(model, edges, sample)
        self.ind = Individual(model, edges)
        self.nodes = edges_to_nodes(edges)
        self.node_count = len(self.nodes)
        
    def get_next(self, states, values):
        new_states = {}
        new_values = {}
        next_conform, next_conform_values = self.conform.get_next(states, values)
        next_ind, next_ind_values = self.ind.get_next(states, values)
        for n in self.nodes:
            if next_ind_values[n] > next_conform_values[n]:
                new_states[n] = next_ind[n]
                new_values[n] = next_ind_values[n]
            else:
                new_states[n] = next_conform[n]
                new_values[n] = next_conform_values[n]
        return new_states, new_values

class LocalIndividual(Strategy):
    
    def __init__(self, model, edges_node_loc, structured=True):
        self.model = model
        self.edges_node_loc = edges_node_loc
        self.nodes = edges_node_loc_to_nodes(edges_node_loc)
        self.node_count = len(self.nodes)
        # Construct node->loc and loc-> node map
        self.node_by_loc = dict([(l, set()) for l in xrange(model.N)])
        self.loc_by_node = dict([(n, set()) for n in self.nodes])
        for edge in edges_node_loc:
            node, loc = edge
            self.node_by_loc[loc].add(node)
            self.loc_by_node[node].add(loc)
        for k, v in self.node_by_loc.iteritems():
            self.node_by_loc[k] = list(v)
        for k, v in self.loc_by_node.iteritems():
            self.loc_by_node[k] = list(v)
        # Set concern loci for each node
        if structured:
            # Use NK structure for choosing hill-climbing loci
            self.concern = [self.loc_by_node[n] for n in self.nodes]
        else:
            # Randomly choose hill-climbing loci
            loci = range(model.N)
            K = model.K
            self.concern = [random.sample(loci, K+1) for n in self.nodes]
        
    def get_next(self, states, values):
        new_states = dict(states)
        new_values = dict(values)
        N = self.model.N
        K = self.model.K
        loci = range(N)
        trial_states, trial_values = self.model.get_hillclimb_values(states, self.concern)
        for n in self.nodes:
            current_value = values[n]
            next_state = states[n]
            next_value = current_value
            node_values = trial_values[n]
            node_states = trial_states[n]
            for i in range(len(self.concern[n])):
                new_value = node_values[i]
                if new_value > next_value:
                    next_state = node_states[i]
                    next_value = new_value
            new_states[n] = next_state
            new_values[n] = next_value
        return new_states, new_values

class LocalConformityIndividual(Strategy):
    
    def __init__(self, model, edges_node_loc, sample=0, structured=True):
        self.model = model
        self.edges = net.affiliation_to_node(edges_node_loc)
        self.conform = Conformity(model, self.edges, sample)
        self.loc_ind = LocalIndividual(model, edges_node_loc, structured)
        self.nodes = edges_node_loc_to_nodes(edges_node_loc)
        self.node_count = len(self.nodes)
        
    def get_next(self, states, values):
        new_states = dict(states)
        new_values = dict(values)
        next_conform, conform_values = self.conform.get_next(states, values)
        next_ind, ind_values = self.loc_ind.get_next(states, values)
        for n in self.nodes:
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
    
    def __init__(self, model, edges_node_loc, sample=0, structured=True):
        self.model = model
        self.edges = net.affiliation_to_node(edges_node_loc)
        self.best = BestNeighbor(model, self.edges, sample)
        self.loc_ind = LocalIndividual(model, edges_node_loc, structured)
        self.nodes = edges_node_loc_to_nodes(edges_node_loc)
        self.node_count = len(self.nodes)
        
    def get_next(self, states, values):
        new_states = dict(states)
        new_values = dict(values)
        next_best, best_values = self.best.get_next(states, values)
        next_ind, ind_values = self.loc_ind.get_next(states, values)
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

class LocalIndividualConsensus(Strategy):
    
    def __init__(self, model, edges_node_loc, sample=0):
        self.model = model
        self.sample = sample
        self.nodes = edges_node_loc_to_nodes(edges_node_loc)
        self.node_count = len(self.nodes)
        # Create node->loc and loc->node mapping
        self.node_by_loc = dict([(l, set()) for l in xrange(model.N)])
        self.loc_by_node = dict([(n, set()) for n in self.nodes])
        for edge in edges_node_loc:
            node, loc = edge
            self.node_by_loc[loc].add(node)
            self.loc_by_node[node].add(loc)
        for k, v in self.node_by_loc.iteritems():
            self.node_by_loc[k] = list(v)
        for k, v in self.loc_by_node.iteritems():
            self.loc_by_node[k] = list(v)
        # Use NK structure for choosing hill-climbing loci
        self.concern = [self.loc_by_node[n] for n in self.nodes]        
    
    def get_next(self, states, values):
        state = states.values()[0]
        state_value = values.values()[0]
        N = self.model.N
        K = self.model.K
        loci = range(N)
        # Each node's private preferred state after individual learning
        best_states = {}
        # Hill climbing for connected subset of NK cells
        trial_states, trial_values = self.model.get_hillclimb_values(states, self.concern)
        for n in self.nodes:
            next_state = list(state)
            next_value = state_value
            node_states = trial_states[n]
            node_values = trial_values[n]
            for i in range(len(self.concern[n])):
                new_value = node_values[i]
                if new_value > next_value:
                    next_value = new_value
                    next_state = node_states[i]
            best_states[n] = next_state
        # Local (per-NK-cell) Consensus
        loc_total = [0] * self.model.N
        loc_count = [0] * self.model.N
        for node, locs in self.loc_by_node.iteritems():
            if self.sample == 0 or len(locs) <= self.sample:
                to_sample = locs
            else:
                to_sample = random.sample(locs, self.sample)
            for l in to_sample:
                loc_count[l] += 1
                loc_total[l] += best_states[node][l]
        next_state = list(state)
        # Majority vote
        for l in range(self.model.N):
            if loc_count[l] == 0 or float(loc_total[l]) / float(loc_count[l]) == 0.5:
                continue
            if float(loc_total[l]) / float(loc_count[l]) > 0.5:
                next_state[l] = 1
            else:
                next_state[l] = 0
        next_value = self.model.get_value(next_state)
        return dict([(n, next_state) for n in self.nodes]), dict([(n, next_value) for n in self.nodes])
        
