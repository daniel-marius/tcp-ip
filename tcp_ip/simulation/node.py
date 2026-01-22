"""TCP/IP Simulation"""

from tcp_ip.layers.datalink import DataLinkLayer
from tcp_ip.layers.network import NetworkLayer
from tcp_ip.layers.transport import TransportLayer
from tcp_ip.layers.application import ApplicationLayer

def build_stack() -> ApplicationLayer:
    """Build TCP/IP stack"""
    datalink = DataLinkLayer()
    network = NetworkLayer(datalink)
    transport = TransportLayer(network)
    return ApplicationLayer(transport)
