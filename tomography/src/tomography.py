import connection
import node

class tomography(object):
    def __init__(self, manual=False, nodes=None, connections=None):
        self.manual = manual
        #xor stand in
        if ((nodes or connections) and not (nodes and connections)) or ((nodes and connections) and (len(nodes) < (len(connections) - 1))):
            raise IndexError
        try:
            if validate_connections(nodes, connections):
                self.nodes = nodes
                self.connections = connections
        except StandardError:
            print("A connection does not have an end or start point")

    def tick(self):
        """Increment all connections by one unit of time."""
        [connection.tick() for connection in self.connections]

    def validate_connections(nodes, connections):
        """Ensure all connections actually connect to a node that has been provided."""
        #nodes may have multiple connections to the same node (this is to allow for data centers/smaller servers)
        if len(nodes) < len(connections) - 1:
            raise IndexError
        names = [node.address for node in nodes]
        for connection in connections:
            if (connection.start_node.address is connection.end_node.address) or connection.start_node.address not in names or connection.end_node.address not in names:
                raise StandardError #addressError
        return True