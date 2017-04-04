import Packet

class Node(object):
    """A node is the [current] base class of an object that connects to the 'Internet'."""
    def __init__(self, connections, address, debugging=True):
        self.address = address
        self.address_split = self.address.split('.')
        self.connections = list(connections)
        self.debug_mode = debugging

    def create_traffic(self, message, target):
        """Generates traffic from this node to a target"""
        data = Packet.Packet(target, self.address, message)
        self.route_traffic(data)

    def recieve_packet(self, packet):
        """Takes a packet from a connection and determines
         its next connection if not the target."""
        if packet.destination is not self.address:
            try:
                self.route_traffic(packet)
            except LookupError:
                print("Cannot route traffic")
        else:
            self.debug(packet.message)

    def route_traffic(self, data):
        """Find the correct node to send a packet to."""
        address = data.destination.split('.')
        #determine if the traffic is downstream or upstream
        destination = self.determine_common_node(address)
        for connection in self.connections:
            if connection.address is destination:
                connection.send_data(self.address, data)
                return
        raise LookupError()

    def determine_common_node(self, target_address):
        """Determine the first node the target and this node share in common"""
        if len(target_address) is not len(self.address_split):
            while len(target_address) > len(self.address_split):
                self.address_split.append(0)
            while len(target_address) < len(self.address_split):
                target_address.append(0)
        for index, this_layer in enumerate(self.address_split):
            if this_layer is not target_address[index]:
                if this_layer is 0:
                    return self.address_split
                if target_address[index] is 0:
                    return target_address
                return target_address[:index] + ([0] * (len(target_address) - index))

    def search(self):
        """Placeholder method that will find a path if the normal methods do not work."""
        pass

    def debug(self, message):
        """Prints messages if debugging is active."""
        if self.debug_mode:
            print(message)
