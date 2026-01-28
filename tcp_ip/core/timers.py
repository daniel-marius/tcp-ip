"""Retransmission Manager"""

import time

class RetransmissionTimer:
    """Retransmission Timer class"""

    def __init__(self, timeout=1.0) -> None:
        self._timeout = timeout
        self._inflight = {} # seq -> (segment, timestamp)

    def ack(self, ack_num: int) -> None:
        """Filter tcp sequence number"""
        self._inflight = {
            seq: v for seq, v in self._inflight.items() if seq >= ack_num
        }

    def expired(self) -> list:
        """Check for expired tcp segments"""
        now = time.time()
        return [
            seg for seg, ts in self._inflight.values()
            if now - ts > self._timeout
        ]

    def track(self, seg) -> None:
        """Keep track of tcp segments"""
        self._inflight[seg.seq] = (seg, time.time())
