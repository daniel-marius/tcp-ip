"""Transport Layer"""

from typing import Any

from tcp_ip.core.interfaces import Layer
from tcp_ip.core.packets import TCPSegment
from tcp_ip.core.protocols import TCPConnection, TCPStateMachine

class TransportLayer(Layer):
    """Transport Layer class"""

    def __init__(self, next_layer: Layer) -> None:
        self._next_layer = next_layer
        self._conn = TCPConnection()
        self._fsm = TCPStateMachine()

    def connect(self) -> None:
        """Define connect method"""
        syn = self._conn.active_open()
        self._next_layer.send(data=syn.serialize())

    def send(self, data: bytes) -> bytes:
        """Send method"""
        segment: TCPSegment = TCPSegment(
            src_port=1234,
            dst_port=80,
            seq=self._conn.seq,
            ack=self._conn.ack,
            flags=0,
            payload=data,
        )
        return self._next_layer.send(data=segment.serialize())

    def receive(self, data: bytes) -> Any:
        """Receive method"""
        segment: TCPSegment = TCPSegment.deserialize(raw=data)
        response = self._fsm.on_receive(conn=self._conn, seg=segment)
        if response:
            self._next_layer.send(data=response.serialize())
        return segment.get("payload", None)
