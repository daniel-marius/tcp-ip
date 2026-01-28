"""Test sliding window"""

from tcp_ip.core.window import SlidingWindow
from tcp_ip.core.packets import TCPSegment

def make_segment(seq, payload=b"x") -> TCPSegment:
    return TCPSegment(
        src_port=1234,
        dst_port=80,
        seq=seq,
        ack=0,
        flags=0,
        payload=payload,
    )


def test_window_allows_send_until_cwnd() -> None:
    window:SlidingWindow = SlidingWindow(mss=100)
    cwnd = 300  # allow 3 segments

    assert window.can_send(cwnd)

    seg1: TCPSegment = make_segment(0, b"a" * 100)
    window.on_send(seg1)

    seg2: TCPSegment = make_segment(100, b"a" * 100)
    window.on_send(seg2)

    seg3: TCPSegment = make_segment(200, b"a" * 100)
    window.on_send(seg3)

    assert not window.can_send(cwnd)


def test_ack_advances_send_base_and_clears_unacked() -> None:
    window: SlidingWindow = SlidingWindow(mss=100)

    seg1: TCPSegment = make_segment(0, b"a" * 100)
    seg2: TCPSegment = make_segment(100, b"a" * 100)

    window.on_send(seg1)
    window.on_send(seg2)

    assert len(window.unacked) == 2

    window.on_ack(100)

    assert window.send_base == 100
    assert len(window.unacked) == 1
    assert 0 not in window.unacked
