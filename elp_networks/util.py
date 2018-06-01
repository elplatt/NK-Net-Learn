def edges_to_weights(edges_from):
    '''Convert edges representation to weights representation.
    edges_from: dict mapping source nodes to sets of targets.
    returns: dict of dicts mapping source to target to weight.'''
    weights_from_to = dict()
    for source, targets in edges_from.iteritems():
        for target in targets:
            weights_from_to[(source,target)] = 1.0
    return weights_from_to
