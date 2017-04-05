INBOUND = 0
OUTBOUND = INBOUND + 1
class Packet(object):
    """Data packet with definitions of the data."""

    def __init__(self, destination, origin, message):
        self.direction = None
        self.destination = destination
        self.origin = origin
        self.message = message
        