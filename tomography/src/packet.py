UPSTREAM = 0
DOWNSTREAM = UPSTREAM + 1
class Packet(object):
    """Data packet with definitions of the data."""

    def __init__(self, destination, origin, message, path=None):
        self.direction = None
        self.destination = destination
        self.origin = origin
        self.message = message
        self.path = path
        self.has_cached = (len(self.path) > 1
                           and self.path[0] is origin and self.path[-1] is destination)

    def log(self, node_address_to_log):
        """Inserts a nodes address onto the log so that it may be cached for later use"""
        if self.has_cached:
            #if a cache exists then we do not want to write additional information
            #that cache will serve as a log
            return
        self.path.append(node_address_to_log)

    def get_reverse_log(self):
        """Gets the reverse of the path taken for the destination node to use."""
        return self.path[::-1]
