"""A Connection is a list of links. Propagates data to and from Nodes."""
import Packet

class Connection(object):
    """Container for Link objects."""
    def __init__(self, start_node, end_node, tapping_nodes=None):
        self.links = [[], []]
        self.start_node = start_node
        self.end_node = end_node
        self.tapping_nodes = []
        self.nodes = [self.start_node, self.end_node] + tapping_nodes
        self.buffer = []
        self.packets_in_buffer = []

    def tick(self, tick=1):
        """Update every link in this connection by 'ticking' time by 'tick' units."""
        for _counter in range(tick):
            for link in self.links:
                self.pass_to_node(link.tick())

    def recieve_packet(self, packet):
        """Takes a pack as input and attaches that packet to the least busy link."""
        if packet:
            try:
                self.best_link().recieve_packet(packet)
                self.packets_in_buffer.append(packet)
            except OverflowError:
                print("Packet drop.")

    def send_packet(self, origin, packet):
        """Send the packet to the link."""
        if origin is self.start_node.address:
            packet.direction = Packet.DOWNSTREAM
        else:
            packet.direction = Packet.UPSTREAM
        self.best_link(packet.direction).recieve_packet(packet)

    def best_link(self, direction):
        """Find the least busy link in this connection."""
        min_index = None
        min_index = 0
        for index, time in enumerate([link.buffer_sum() for link in self.links[direction]]):
            if not min_index:
                min_index = time
            elif min_index > time:
                min_index = index
        return self.links[direction][min_index]

    def add_link(self, link=None, links=None):
        """Add a link and/or links to this connection."""
        #flexible to allow to for a list of links or a single object.
        if not links:
            links = []
        links.append(link)
        for new_link in links:
            pos = Packet.UPSTREAM if new_link.start_node is self.end_node else Packet.UPSTREAM
            #add a link to upstream or downstream links
            self.links[pos].append(new_link)

    def pass_to_node(self, packet):
        """Give data to the node that the data did not come from.
        Also pass to tapping nodes"""
        for tap in self.tapping_nodes:
            tap.recieve_packet.append(packet)
        if packet.direction is Packet.UPSTREAM:
            self.start_node.recieve_packet(packet)
        if packet.direction is Packet.DOWNSTREAM:
            self.end_node.recieve_packet(packet)

    def end_point(self, node_address):
        """Checks if a given address is a start or end point of this Connection."""
        return node_address is self.end_node or node_address is self.start_node

    def connected(self, node1_address, node2_address):
        """Checks if this connection connect node1 to node2?"""
        return self.end_point(node1_address) and self.end_point(node2_address)
