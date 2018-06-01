
def floyd_warshall(weights_from_to):
    '''Find shortest paths between all edge pairs in a weighted graph with no negative cycles.
    weights_from_to: dict of mapping (source, target) pairs to their edge weights.
    returns: (distances, paths)
        distances: maps (source, target) node pairs to their shortest path distance.
        paths: maps (source, target) node pairs to a list of shortest paths. Each path is a list
            of intermediate nodes (without the source or target node).
    '''
    # Create sorted list of nodes
    nodes = set()
    for edge, weight in weights_from_to.iteritems():
        source, target = edge
        nodes.add(source)
        nodes.add(target)
    nodes = sorted(nodes)
    node_index = dict([(node, i) for i, node in enumerate(nodes)])
    # Initialize distances and paths
    # For each source, target, there is a list of shortest paths (there may be multiple of the same length)
    dist = [[float("inf") for target in nodes] for source in nodes]
    paths = [[ [] for target in nodes] for source in nodes]
    for k, node in enumerate(nodes):
        dist[k][k] = 0
        paths[k][k].append([])
    for edge, weight in weights_from_to.iteritems():
        source, target = edge
        i = node_index[source]
        j = node_index[target]
        dist[i][j] = weight
        paths[i][j].append([])
    # Use only first k nodes
    for k, node in enumerate(nodes):
        # Loop through pairs
        for i, source in enumerate(nodes):
            for j, target in enumerate(nodes):
                if i == j or i == k or j == k:
                    # Ignore if endpoints are the same
                    # or if intermediate node is one of the endpoints
                    continue
                # Find shortest path using k
                dist_k = dist[i][k] + dist[k][j]
                # Find shortest path not using k
                dist_nok = dist[i][j]
                if dist_k < dist_nok:
                    # Set new distance
                    dist[i][j] = dist_k
                    paths_ij = []
                    # Add new paths
                    for ipath in paths[i][k]:
                        for jpath in paths[k][j]:
                            # Merge paths
                            newpath = ipath + [k] + jpath
                            paths_ij.append(newpath)
                    # Replace old paths
                    paths[i][j] = paths_ij
                elif dist_k == dist_nok:
                    # Same distance, but new paths
                    # Store path list for better performance
                    paths_ij = paths[i][j]
                    for ipath in paths[i][k]:
                        for jpath in paths[k][j]:
                            # Merge paths
                            newpath = ipath + [k] + jpath
                            paths_ij.append(newpath)
    # Convert distances and paths from indexes to labels
    dist_dict = {}
    path_dict = {}
    for i, source in enumerate(nodes):
        dist_dict[source] = {}
        path_dict[source] = {}
        for j, target in enumerate(nodes):
            dist_dict[source][target] = dist[i][j]
            path_dict[source][target] = [[nodes[n] for n in path] for path in paths[i][j]]
    return (dist_dict, path_dict)