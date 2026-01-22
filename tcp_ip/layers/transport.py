"""Transport Layer"""

from tcp_ip.core.interfaces import Layer
from tcp_ip.core.packets import TCPSegment

class TransportLayer(Layer):
    """Transport Layer class"""

    def __init__(self, next_layer: Layer) -> None:
        self._next_layer = next_layer

    def send(self, data: bytes) -> bytes:
        """Send method"""
        segment = TCPSegment(
            src_port=1234,
            dst_port=80,
            seq=1,
            ack=0,
            payload=data
        )
        return self._next_layer.send(segment.serialize())

    def receive(self, data: bytes) -> bytes:
        """Receive method"""
        segment = TCPSegment.deserialize(data)
        return segment.get("payload", None)
