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
    for n in range(model.N):
        for i in range(nodes_per_locus):
            for d in model.dependence[n]:
                edges_node_loc.append( (node, d) )
            node += 1
    return edges_node_loc

def rewire_affiliation(model, edges_node_loc, rewire):
    # Rewire the node-locus affiliation network        
    rewire_count = int(len(edges_node_loc) * rewire)
    to_rewire = random.sample(range(len(edges_node_loc)), rewire_count)
    for e in to_rewire:
        edge = edges_node_loc[e]
        node = edge[0]
        new_loc = random.choice(range(model.N))
        edges_node_loc[e] = (node, new_loc)

def affiliation_to_node(edges_node_loc):
    # Construct node-node network
    node_by_loc = {}
    loc_by_node = {}
    for edge in edges_node_loc:
        node, loc = edge
        try:
            node_by_loc[loc].append(node)
        except KeyError:
            node_by_loc[loc] = [node]
        try:
            loc_by_node[node].append(loc)
        except KeyError:
            loc_by_node[node] = [loc]
    edges_node = {}
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
