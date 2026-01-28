"""Test Congestion Control"""

from tcp_ip.core.congestion import CongestionControl

def test_slow_start_growth() -> None:
    cc: CongestionControl = CongestionControl(mss=1000)

    assert cc.cwnd == 1000

    cc.on_ack()
    assert cc.cwnd == 2000

    cc.on_ack()
    assert cc.cwnd == 3000


def test_congestion_avoidance_growth() -> None:
    cc: CongestionControl = CongestionControl(mss=1000)
    cc.ssthresh = 2000
    cc.cwnd = 2000

    cc.on_ack()
    assert cc.cwnd > 2000
    assert cc.cwnd < 3000  # linear-ish growth


def test_timeout_collapses_cwnd() -> None:
    cc: CongestionControl = CongestionControl(mss=1000)
    cc.cwnd = 8000

    cc.on_timeout()

    assert cc.ssthresh == 4000
    assert cc.cwnd == 1000
