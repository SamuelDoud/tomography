import datetime

class connection(object):
    
    def __init__(self, start_node, end_node, weight):
        self.end_node = end_node
        self.start_node = start_node
        self.weight = weight
        self.nodes = [self.start_node, self.end_node]
        self.connection_queue = []
        
    def send_data(self, address_from, data):
        item =(data, datetime.datetime.now, address_from)
        self.connection_queue.append(item)

    def update(self):
        if self.connection_queue:
            if self.connection_queue[0][1] + datetime.timedelta(milliseconds=self.weight) >= datetime.datetime.now():
                self.pass_data(self.connection_queue[0][0], self.connection_queue[0][2])
                self.connection_queue.pop(0)
                if self.connection_queue:
                    self.connection_queue[0][1] = datetime.datetime.now()

    def pass_data(self, data, address_from):
        for n in self.nodes:
            if n.address is not address_from:
                n.recieve(data)
