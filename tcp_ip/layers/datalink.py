"""DataLink Layer"""

from tcp_ip.core.interfaces import Layer

class DataLinkLayer(Layer):
    """DataLink Layer"""

    def send(self, data: bytes) -> bytes:
        """Send method"""
        return data  # simulate wire transmission

    def receive(self, data: bytes) -> bytes:
        """Receive method"""
        return data
