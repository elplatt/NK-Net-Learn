def to_nx(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def makeGraph(cls, m):
    import networkx as nx
    net = cls(m)
    G = to_nx(net.nodes, net.edges)
    del net
    return G
    