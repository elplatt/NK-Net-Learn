
class Network(object):
    """Base class for network objects."""
    
    def __init__(self):
        pass

    def edges(self):
        for source in self.nodes():
            for target in self.neighbors(source):
                yield (source, target)