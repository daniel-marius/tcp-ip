"""Test packets"""

import pytest
from tcp_ip.core.packets import TCPSegment

def test_invalid_port() -> None:
    """Test TCP invalid port"""
    with pytest.raises(ValueError):
        TCPSegment(
            src_port=70000,
            dst_port=80,
            seq=1,
            ack=0,
        )
