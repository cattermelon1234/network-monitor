"""from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.http import HTTP
from scapy.layers import http
"""
import pyshark
from ConnectionAnalyzer import ConnectionAnalyzer

class RealTimeMonitor:
    def __init__(self):
        pass

    def analyze(self, network_interface):
        capture = pyshark.LiveCapture(interface=network_interface)
        connection_analyzer = ConnectionAnalyzer()
        for raw_packet in capture.sniff_continuously():
            if hasattr(raw_packet, 'tcp') or hasattr(raw_packet, 'udp') and hasattr(raw_packet, 'ip'):
                try:
                    # Get the timestamp when the packet was captured
                    timestamp = float(raw_packet.sniff_timestamp)  # PyShark provides this as a Unix timestamp
                    connection_analyzer.analyze(timestamp, raw_packet)

                except Exception as e:
                    
                    print(f"Error processing packet: {e}")

    def get_packet_details(self, packet):
        protocol = packet.transport_layer
        source_address = packet.ip.src
        source_port = packet[packet.transport_layer].srcport
        destination_address = packet.ip.dst
        destination_port = packet[packet.transport_layer].dstport
        packet_time = packet.sniff_time
        return f'Packet Timestamp: {packet_time}' \
            f'\nProtocol type: {protocol}' \
            f'\nSource address: {source_address}' \
            f'\nSource port: {source_port}' \
            f'\nDestination address: {destination_address}' \
            f'\nDestination port: {destination_port}\n'


    def filter_all_tcp_traffic_file(self, packet):
        if hasattr(packet, 'tcp') or hasattr(packet, 'udp'):
            results = self.get_packet_details(packet)
        return results