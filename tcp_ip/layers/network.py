"""Network Layer"""

from tcp_ip.core.interfaces import Layer

class NetworkLayer(Layer):
    """Network Layer class"""

    def __init__(self, next_layer: Layer) -> None:
        self._next_layer = next_layer

    def send(self, data: bytes) -> bytes:
        """Send method"""
        return self._next_layer.send(data)

    def receive(self, data: bytes) -> bytes:
        """Receive method"""
        return data
