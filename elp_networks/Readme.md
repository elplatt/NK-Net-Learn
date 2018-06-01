# Network generators

This package generates different kinds of networks.
All objects have a `nodes` set containing integer node ids,
as well as an `edges` set containing frozensets of node ids.

Currently available networks are:
* Cube(m): An m-dimensional cube

## Example usage
Creating a generator:

    import networks
    net = networks.Cube(2)
    
    print net.nodes
    #=> set(0, 1, 2, 3)
    
    print net.edges
    #=> set(
    #     frozenset([0, 1]),
    #     frozenset([1, 3]),
    #     frozenset([3, 2]),
    #     frozenset([2, 0]))
