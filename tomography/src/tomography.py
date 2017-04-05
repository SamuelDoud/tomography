class Tomography(object):
    """Main class to operate the network. Will control all nodes, connections, and increments."""
    def __init__(self, manual=False, nodes=None, connections=None):
        self.manual = manual
        #xor stand in
        if (((nodes or connections) and not (nodes and connections))
                or ((nodes and connections) and (len(nodes) < (len(connections) - 1)))):
            raise IndexError
        try:
            if validate_connections(nodes, connections):
                self.nodes = nodes
                self.connections = connections
        except AttributeError:
            print("A connection does not have an end or start point")

    def tick(self):
        """Increment all connections by one unit of time."""
        return [connection.tick() for connection in self.connections]

def validate_connections(nodes, connections):
    """Ensure all connections actually connect to a node that has been provided."""
    #nodes may have multiple connections to the same node
    #(this is to allow for data centers/smaller servers)
    if len(nodes) < len(connections) - 1:
        #There can't be no nodes then connections less 1
        raise IndexError
    names = [node.address for node in nodes]
    for connection_obj in connections:
        if (connection_obj.start_node.address is connection_obj.end_node.address
                or connection_obj.start_node.address not in names
                or connection_obj.end_node.address not in names):
            raise AttributeError #addressError
    return True
