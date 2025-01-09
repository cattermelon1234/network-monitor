class Connection:
    def __init__(self, packet):
        self.protocol = packet.transport_layer
        self.source_ip = packet.ip.src
        self.destination_ip = packet.ip.dst
    
    def __eq__(self, other):
        return (self.source_ip == other.source_ip and self.destination_ip == other.destination_ip) or \
        (self.source_ip == other.destination_ip and self.destination_ip == other.source_ip) and \
        self.protocol == other.protocol

    def __hash__(self):
        return hash((self.protocol, self.source_ip, self.destination_ip))

    
        