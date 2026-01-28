"""Sliding Window for TCP"""

class SlidingWindow:
    """Sliding Window class"""

    def __init__(self, mss=1000) -> None:
        self._mss = mss
        self._send_base = 0
        self._next_seq = 0
        self._unacked = {}  # seq -> segment

    @property
    def mss(self) -> int:
        """mss getter"""
        return self._mss

    @property
    def next_seq(self) -> int:
        """next_seq getter"""
        return self._next_seq

    @property
    def send_base(self) -> int:
        """send_base getter"""
        return self._send_base

    @property
    def unacked(self) -> dict:
        """unacked getter"""
        return self._unacked

    def can_send(self, cwnd):
        """Check if can send"""
        return (self._next_seq - self._send_base) < cwnd

    def on_send(self, seg) -> None:
        """On send method"""
        self._unacked[seg.seq] = seg
        self._next_seq += len(seg.payload)

    def on_ack(self, ack_num: int) -> None:
        """On ack method"""
        to_remove = [
            seq for seq in self._unacked if seq < ack_num
        ]
        for seq in to_remove:
            del self._unacked[seq]
        self._send_base = ack_num
