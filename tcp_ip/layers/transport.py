"""Transport Layer"""

from typing import Any

from tcp_ip.core.congestion import CongestionControl
from tcp_ip.core.interfaces import Layer
from tcp_ip.core.packets import TCPSegment
from tcp_ip.core.protocols import TCPConnection, TCPStateMachine
from tcp_ip.core.timers import RetransmissionTimer
from tcp_ip.core.window import SlidingWindow

class TransportLayer(Layer):
    """Transport Layer class"""

    def __init__(self, next_layer: Layer) -> None:
        self._next_layer = next_layer
        self._conn = TCPConnection()
        self._fsm = TCPStateMachine()
        self._timer = RetransmissionTimer()
        self._window = SlidingWindow()
        self._congestion = CongestionControl()

    def on_ack(self, ack_num: int) -> None:
        """On ack method"""
        self._window.on_ack(ack_num)
        self._timer.ack(ack_num)
        self._congestion.on_ack()

    def connect(self) -> None:
        """Define connect method"""
        syn = self._conn.active_open()
        self._next_layer.send(data=syn.serialize())

    def send(self, data: bytes) -> bytes:
        """Send method"""
        offset = 0
        while offset < len(data):
            if not self._window.can_send(self._congestion.cwnd):
                break

            chunk = data[offset:offset + self._window.mss]
            seg = TCPSegment(
                src_port=1234,
                dst_port=80,
                seq=self._window.next_seq,
                ack=self._conn.ack,
                flags=0,
                payload=chunk,
            )

            self._window.on_send(seg)
            self._timer.track(seg)
            self._next_layer.send(seg.serialize())

            offset += len(chunk)

    def receive(self, data: bytes) -> Any:
        """Receive method"""
        segment: TCPSegment = TCPSegment.deserialize(raw=data)
        response = self._fsm.on_receive(conn=self._conn, seg=segment)
        if response:
            self._next_layer.send(data=response.serialize())
        return segment.get("payload", None)

    def tick(self) -> None:
        """Send unacknowledged tcp segments"""
        for seg in self._timer.expired():
            self._congestion.on_timeout()
            self._timer.track(seg)
            self._next_layer.send(seg.serialize())
