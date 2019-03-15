from elp_networks.algorithms.shortest_paths import floyd_warshall

def betweenness(weights_from_to, normalized=True, distances=None, paths=None):
    nodes = set()
    for edge, weight in weights_from_to.iteritems():
        source, target = edge
        nodes.add(source)
        nodes.add(target)
    if normalized:
        norm = float(
            (len(nodes) - 1) * (len(nodes) - 2)
            )
    else:
        norm = 1.0
    # Calculate shortest paths if they haven't been passed in
    if distances is None:
        distances, paths = floyd_warshall(weights_from_to)
    result = dict([(n, 0.0) for n in paths.keys()])
    for source, targets in paths.iteritems():
        for target, pair_paths in targets.iteritems():
            count = float(len(pair_paths))
            for p in pair_paths:
                for node in p:
                    try:
                        result[node] += 1.0/count/norm
                    except KeyError:
                        result[node] = 1.0/count/norm
    return result

def recalculated_betweenness(weights_from_to, normalized=True):
    initial = betweenness(weights_from_to, normalized=normalized)
    remaining = sorted(list(initial.iteritems()), key=lambda x:x[1])
    while len(remaining) > 0:
        label, centrality = remaining.pop()
        if centrality == 0:
            # No more nonzero centralities
            return
        yield (label, centrality)
        for edge in weights_from_to.keys():
            if label in edge:
                del weights_from_to[edge]
        result = betweenness(weights_from_to, normalized=normalized)
        remaining = sorted(list(result.iteritems()), key=lambda x:x[1])