class Link(object):
    """Handles packet transfer from node-to-node based controlled by a Connection."""

    def __init__(self, start_node, end_node, weight, buffer_size=10):
        self.end_node = end_node
        self.start_node = start_node
        self.weight = weight
        self.nodes = [self.start_node, self.end_node]
        self.buffer = []
        self.in_link = [None] * self.weight
        self.buffer_size = buffer_size
        self.data_bubble = None

    def recieve_packet(self, data):
        """Takes a packet from the connection and keeps it until it has passed through the link."""
        if len(self.buffer) > self.buffer_size:
            # The buffer is full and the packet will be dropped if not handled.
            #raise OverflowError
            return
        self.buffer.append(data)

    def tick(self):
        """Update the buffer by decrementing the time on the top link by one."""
        self.data_bubble = None
        if self.buffer:
            # the packet has now reached its destination
            self.in_link.append(self.buffer[0])
            self.buffer = self.buffer[1:]
        else:
            self.in_link.append(None)
        self.pass_packet()
        return self.data_bubble

    def pass_packet(self):
        """Simple method to propagate the data that just passed through the
         link to the connection."""
        self.data_bubble = self.in_link[0]
        self.in_link = self.in_link[1:]
        return self.data_bubble

    def buffer_sum(self):
        """Get the number of ticks required to clear the buffer.
        Also ensure that the buffer isn't full!"""
        if len(self.buffer) == self.buffer_size:
            # just pass up None to indicate that the buffer is full and there
            # is no legal wait time.
            return None
        wait_time = len(self.buffer) * self.weight
        return wait_time
