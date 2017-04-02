import packet

class node(object):
    def __init__(self, address, connections):
        self.address = address
        self.address_split = self.address.split('.')
        self.connections = list(connections)

    def create_traffic(self, message, target):
        data = packet(self.address, target, message)
        route_traffic(data)

    def recieve(self, data):
        if data.address is not self.address:
            try:
                self.route_traffic(data)
            except LookupError:
                print("Cannot route traffic")

    def route_traffic(self, data):
        address = data.destination.split('.')
        #determine if the traffic is downstream or upstream
        destination = self.determine_common_node(address)
        for connection in self.connections:
            if connection.address is destination:
                connection.send_data(self.address, data)
                return
        raise LookupError()

    def determine_common_node(self, target_address):
        if len(target_address) is not len(self.address_split):
            while len(target_address) > len(self.address_split):
                self.address_split.append(0)
            while len(target_address) < len(self.address_split):
                self.target_address.append(0)
        for index, this_layer in enumerate(self.address_split):
            if this_layer is not target_address[index]:
                if this_layer is 0:
                    return self.address_split
                if target_address[index] is 0:
                    return target_address
                return (target_address[:index] + ([0] * (len(target_address) - index)))

    def search(self):
        pass