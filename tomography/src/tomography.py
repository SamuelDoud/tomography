"""Controls the Network in a God-like manner."""
import Connection

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
        self.nodes = [] + nodes
        self.connections = [] + connections

    def remove_node(self, node):
        """Removes the node from the list of Nodes and removes any connections that
         contain node as a start or end Node."""
        self.nodes.remove(node)
        for index, connection in enumerate(self.connections):
            if connection.end_point(node.address):
                self.connections.pop(index)

    def add_node(self, node):
        """Add a node to the node list."""
        self.nodes.append(node)

    def add_connection(self, node1, node2, links=None):
        """Add a connection between two nodes so long a they are already not connected."""
        if not self.neighbors(node1, node2):
            conn = Connection.Connection(node1, node2)
            for link in links:
                conn.add_link(link)
            node1.add_connection(conn)
            node2.add_connection(conn)


    def neighbors(self, node1, node2):
        """Checks if two Nodes are immediately adjacent to eachother."""
        for connection in self.connections:
            if connection.connected(node1, node2):
                return True
        return False

    def tick(self):
        """Increment all connections by one unit of time."""
        for node in self.nodes:
            node.generate_traffic()
        for connection in self.connections:
            connection.tick()

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
