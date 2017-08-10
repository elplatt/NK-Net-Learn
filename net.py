import random

def nk_to_network(model, nodes_per_locus, rewire=0):
    edges_node_loc = nk_to_affiliation(model, nodes_per_locus)
    if rewire > 0:
        rewire_affiliation(model, edges_node_loc, rewire)
    edges_node = affiliation_to_node(edges_node_loc)
    return edges_node

def nk_to_affiliation(model, nodes_per_locus):
    # Construct affilation network connecting each node to a locus and its neighbors
    edges_node_loc = []
    node = 0
    reverse = False
    if reverse:
        # Construct reverse map for NK dependence
        rev_dependence = {}
        for n in range(model.N):
            for d in model.dependence[n]:
                try:
                    rev_dependence[d].add(n)
                except KeyError:
                    rev_dependence[d] = set([n])
    # Add affiliation edges
    for n in range(model.N):
        for i in range(nodes_per_locus):
            # Main NK locus
            edges_node_loc.append( (node, n) )        
            # Follow forward NK edges
            for d in model.dependence[n]:
                edges_node_loc.append( (node, d) )
            if reverse:
                # Follow reverse NK edges
                try:
                    for d in rev_dependence[n]:
                        edges_node_loc.append( (node, d) )
                except KeyError:
                    pass
            node += 1
    return edges_node_loc

def rewire_affiliation(model, edges_node_loc, rewire):
    # Rewire the node-locus affiliation network        
    rewire_count = int(len(edges_node_loc) * rewire)
    # Ensure multiple of 2
    rewire_count = int(rewire_count / 2.0) * 2
    # Get shuffled sample of edges
    to_rewire = random.sample(range(len(edges_node_loc)), rewire_count)
    random.shuffle(to_rewire)
    # Split sample in two and swap locations
    sources = to_rewire[:len(to_rewire)/2]
    targets = to_rewire[len(to_rewire)/2:]
    for e in sources:
        t = targets.pop()
        source_node, source_loc = edges_node_loc[e]
        target_node, target_loc = edges_node_loc[t]
        edges_node_loc[e] = (source_node, target_loc)
        edges_node_loc[t] = (target_node, source_loc)

def affiliation_to_node(edges_node_loc):
    '''Construct node-node network from node-locus network.'''
    # Create node->loc and loc-> node maps
    node_by_loc = {}
    loc_by_node = {}
    for edge in edges_node_loc:
        node, loc = edge
        try:
            node_by_loc[loc].add(node)
        except KeyError:
            node_by_loc[loc] = set([node])
        try:
            loc_by_node[node].add(loc)
        except KeyError:
            loc_by_node[node] = set([loc])
    edges_node = {}
    # For a source node and its loci, create edges to/from other nodes
    # dependent on those loci
    for source, loci in loc_by_node.iteritems():
        for loc in loci:
            for target in node_by_loc[loc]:
                if source == target:
                    continue
                try:
                    edges_node[source].add(target)
                except KeyError:
                    edges_node[source] = set([target])
                try:
                    edges_node[target].add(source)
                except KeyError:
                    edges_node[target] = set([source])                   
    return edges_node

def sample_edges(edges, p):
    '''Keep fraction p of edges.'''
    n = int(round(float(sum([len(v) for v in edges.values()]) * p)))
    edge_pairs = sum([[(s,t) for t in edges[s]] for s in edges.keys()], [])
    new_edge_pairs = random.sample(edge_pairs, n)
    new_edges = {}
    for s,t in new_edge_pairs:
        try:
            new_edges[s].add(t)
        except KeyError:
            new_edges[s] = set([t])
    return new_edges