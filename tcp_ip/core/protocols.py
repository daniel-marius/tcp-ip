"""Protocols"""

from typing import Any
from enum import Enum, auto
from tcp_ip.core.packets import TCPSegment, TCPFlags

class TCPState(Enum):
    """TCPSTate class"""
    CLOSED = auto()
    LISTEN = auto()
    SYN_SENT = auto()
    SYN_RECEIVED = auto()
    ESTABLISHED = auto()
    FIN_WAIT_1 = auto()
    FIN_WAIT_2 = auto()
    TIME_WAIT = auto()


class TCPConnection:
    """TCP Connection class"""
    def __init__(self) -> None:
        self._state = TCPState.CLOSED
        self._seq = 0
        self._ack = 0

    @property
    def ack(self) -> int:
        """Ack getter"""
        return self._seq

    @property
    def seq(self) -> int:
        """Seq getter"""
        return self._seq

    @property
    def state(self) -> TCPState:
        """State getter"""
        return self._state

    @ack.setter
    def ack(self, value: Any) -> None:
        """Ack setter"""
        self._ack = value

    @seq.setter
    def seq(self, value: Any) -> None:
        """Seq setter"""
        self._seq = value

    @state.setter
    def state(self, value: Any) -> None:
        """State setter"""
        self._state = value

    def passive_open(self) -> None:
        """Open TCP state"""
        self._state = TCPState.LISTEN

    def active_open(self) -> TCPSegment:
        """Active TCP connection"""
        self._state = TCPState.SYN_SENT
        self._seq += 1
        return TCPSegment(
            src_port=1234,
            dst_port=80,
            seq=self._seq,
            ack=0,
            flags=TCPFlags.SYN,
        )


class TCPStateMachine: # pylint: disable=too-few-public-methods
    """TCP State Machine class"""

    def on_receive(self, conn: TCPConnection, seg: TCPSegment) -> TCPSegment | None:
        """Receive TCP Segment"""
        if conn.state == TCPState.LISTEN and seg.flags & TCPFlags.SYN:
            conn.state = TCPState.SYN_RECEIVED
            conn.seq += 1
            conn.ack = seg.seq + 1

            return TCPSegment(
                src_port=seg.dst_port,
                dst_port=seg.src_port,
                seq=conn.seq,
                ack=conn.ack,
                flags=TCPFlags.SYN | TCPFlags.ACK,
            )

        if conn.state == TCPState.SYN_SENT and seg.flags == (TCPFlags.SYN | TCPFlags.ACK):
            conn.state = TCPState.ESTABLISHED
            conn.ack = seg.seq + 1
            conn.seq += 1

            return TCPSegment(
                src_port=seg.dst_port,
                dst_port=seg.src_port,
                seq=conn.seq,
                ack=conn.ack,
                flags=TCPFlags.ACK,
            )

        if conn.state == TCPState.ESTABLISHED and seg.flags & TCPFlags.FIN:
            conn.state = TCPState.FIN_WAIT_1
            conn.ack = seg.seq + 1

            return TCPSegment(
                src_port=seg.dst_port,
                dst_port=seg.src_port,
                seq=conn.seq,
                ack=conn.ack,
                flags=TCPFlags.ACK | TCPFlags.FIN,
            )

        return None
