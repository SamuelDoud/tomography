"""Object that defines a Node on the network to create, consume, and diseminate data
throughout the network."""

import random
import collections

import Packet
import PingInfo

class Node(object):
    """A node is the [current] base class of an object that connects to the 'Internet'."""
    def __init__(self, connections=None, address=None, *, debugging=True):
        self.address = address
        if self.address:
            self.address_split = self.address.split('.')
        self.connections = list(connections) if connections else []
        if self.connections:
            self.connections[0] = [self.connections[0]]
        else:
            self.connections.append([])
        self.debug_mode = debugging
        self.paths_cache = {}
        self.ping_info_cache = []
        self.tick_number = 0
        self.address_counter = -1

    def generate_traffic(self, target_node_address, message=""):
        """Generates traffic from this node to a target.
        This is the method called to tick the model forward."""
        self.tick_number += 1
        data = Packet.Packet(target_node_address, self.address, message)
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
            self.paths_cache[packet.origin] = packet.get_reverse_log
            if packet.ping_msg:
                if packet.ping_back:
                    self.add_to_ping_stats(packet)
                else:
                    temp = packet.origin
                    packet.origin = packet.destination
                    packet.destination = temp
                    packet.ping_back = True
                    packet.log = [] #maybe make the reverse of the log the cache...
                    #send the ping back to the user
                    self.route_traffic(packet)
            self.debug(packet.message)

    def route_traffic(self, packet):
        """Find the correct node to send a packet to."""
        if packet.has_cached:
            destination = packet.log.index(self.address) + 1
        else:
            address = packet.destination.split('.')
            #determine if the traffic is downstream or upstream
            destination = self.determine_common_node(address)
        for connection in self.connections:
            if connection.address is destination:
                #The Node to route traffic to has been found
                #send traffic to it and end the search.
                connection.send_data(self.address, packet)
                return
        #if this no connection is found then this code will be reached
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
        """Placeholder method that will find a path if the normal methods
        (determine_common_node) do not work."""
        pass

    def debug(self, message):
        """Prints messages if debugging is active."""
        if self.debug_mode:
            print(message)

    def add_connection(self, connection, is_parent):
        """Add a Connection to this Node.
        This allows for the Node to calculate an address."""
        if not isinstance(self.connections[0], collections.Iterable):
            self.connections[0] = [self.connections[0]]
        if is_parent:
            self.connections[0].append(connection)
            if not self.address:
                self.assign_address()
        else:
            #add the parent connection to the first spot
            self.connections.append(connection)

    def remove_connection(self, connection):
        """Delete a connection from the Node.
        If the Node used to generate the Address was selected, reassign the address"""
        index = self.connections.index(connection)
        if index > 0:
            self.connections.pop(connection)
        if index is 0:
            #No longer connected to any other Node. Delete its address
            self.address = None

    def assign_address(self, override=None):
        """Give this Node an address based on the first upstream Node we find.
        If no upstream nodes exist, assign the value of the incrementer.
        The incrementer is the number that will be assigned to nodes with no upstream members
        (in other words, the center of the network)."""
        if override:
            self.address = override
        parent = self.connections[0][0]
        self.address = parent.address + '.' + len(parent.connections)
        self.address_split = self.address.split('.')

    def construct_address(self, upstream_node):
        """Give this node an address based on an upstream node"""
        address_ending = upstream_node.add_downstream()
        self.address = upstream_node.address + "." + address_ending

    def add_downstream(self):
        """Get the next index to assign a node"""
        self.address_counter += 1
        return self.address_counter

    def ping(self, target_address):
        """Sends a message to another node in order to determine the time to that node"""
        ping_packet = Packet.Packet(self.address, target_address, ping_msg=self.tick_number)
        self.route_traffic(ping_packet)

    def add_to_ping_stats(self, ping_packet):
        """Add the results of a ping to the statistics of the node."""
        time_to_respond = self.tick_number - ping_packet.ping_msg
        target_address = ping_packet.origin
        paths = ping_packet.path
        for ping_info_cache_item in self.ping_info_cache:
            if target_address is ping_info_cache_item.target:
                ping_info_cache_item.add_to_stats(time_to_respond, paths)
                return
        self.ping_info_cache.append(PingInfo.PingInfo(target_address))
        self.ping_info_cache[-1].add_to_stats(time_to_respond, paths)

    def ping_dump(self):
        message = [ping.information_summary for ping in self.ping_info_cache]



class EndUser(Node):
    """An EndUser is a Node that is analogous to a consumer of information."""
    def __init__(self, connections, address, *, debugging=True, traffic_chance=0.1):
        super().__init__(self, connections, address, debugging)
        if traffic_chance > 0 and traffic_chance <= 1:
            self.traffic_chance = traffic_chance
        else:
            traffic_chance = 0
        self.popular_nodes = []

    def add_popular_node(self, server, level=1):
        """Add a Node to the list of popular nodes with a level of popularity (chance that any
         connection will go to it)"""
        self.popular_nodes.append((server, level))

    def generate_traffic(self, target_node_address, message=""):
        """Determines whether to send traffic or not."""
        if random.random < self.traffic_chance:
            super().generate_traffic(self.pick_server().address, message="")

    def pick_server(self):
        """Pick a random server based on the relative popularity of all servers to this node."""
        servers, levels = zip(*self.popular_nodes)
        level_sum = sum(levels)
        selection = random.randint(1, level_sum)
        count = 0
        for index, level in enumerate(levels):
            count += level
            if count >= selection:
                return servers[index]

class Server(Node):
    """A server is a node that generates more traffic than it recieves.
    Think of a Netflix or a Facebook. They send more to their users than vice-versa."""
    def init(self, connections, address, *, debugging=True, traffic_level=10, std_dev=3):
        """"Creates a Server instance of a Node."""
        super().__init__(self, connections, address, debugging)
        self.traffic_level, self.std_dev = 0, 0
        if traffic_level > 0:
            self.traffic_level = traffic_level
        if std_dev > 0:
            self.std_dev = std_dev

    def determine_traffic_intensity(self):
        """Return the integer number of packets that will be created by this server to
        a node trying to connect to this server"""
        return random.gauss(self.traffic_level, self.std_dev)

    def generate_traffic(self, target_node_address, message=""):
        """Generate a number of packets to send to another Node."""
        for packet_number in range(self.determine_traffic_intensity):
            packet = Packet.Packet(target_node_address, self.address, message + packet_number)
            super().route_traffic(packet)

    def recieve_packet(self, packet):
        """Gets a message from another node and fires back a many packets."""
        super().debug(packet.message)
        self.generate_traffic(packet.origin, "Responding to " + packet.message + ". ")

