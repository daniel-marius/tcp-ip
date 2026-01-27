"""Test binary codec"""

from tcp_ip.core.packets import TCPSegment, TCPFlags

def test_binary_roundtrip() -> None:
    seg: TCPSegment = TCPSegment(
        src_port=1,
        dst_port=2,
        seq=100,
        ack=50,
        flags=TCPFlags.SYN,
        payload=b"abc",
    )

    raw: bytes = seg.serialize()
    parsed: TCPSegment = TCPSegment.deserialize(raw=raw)

    assert parsed == seg
