"""TCP Congestion Control"""

class CongestionControl:
    """Congestion Control class"""

    def __init__(self, mss=1000) -> None:
        self._mss = mss
        self._cwnd = mss
        self._ssthresh = 64000

    @property
    def cwnd(self) -> int:
        """cwnd getter"""
        return self._cwnd

    @property
    def mss(self) -> int:
        """mss getter"""
        return self._mss

    @property
    def ssthresh(self) -> int:
        """ssthresh getter"""
        return self._ssthresh

    @cwnd.setter
    def cwnd(self, value) -> None:
        """cwnd setter"""
        self._cwnd = value

    @ssthresh.setter
    def ssthresh(self, value) -> None:
        """ssthresh setter"""
        self._ssthresh = value

    def on_ack(self) -> None:
        """On ack method"""
        if self._cwnd < self._ssthresh:
            # Slow start
            self._cwnd += self._mss
        else:
            # Congestion avoidance
            self._cwnd += (self._mss * self._mss) // self._cwnd

    def on_timeout(self) -> None:
        """On timeout method"""
        self._ssthresh = max(self._cwnd // 2, self._mss)
        self._cwnd = self._mss
