"""Test three way handshake"""

from tcp_ip.core.protocols import TCPConnection, TCPSegment, TCPStateMachine, TCPState
from tcp_ip.core.packets import TCPFlags

def test_three_way_handshake() -> None:
    client: TCPConnection = TCPConnection()
    server: TCPConnection = TCPConnection()
    fsm: TCPStateMachine = TCPStateMachine()

    server.passive_open()
    syn: TCPSegment = client.active_open()

    syn_ack: TCPSegment | None = fsm.on_receive(server, syn)
    ack: TCPSegment | None = fsm.on_receive(client, syn_ack)

    assert client.state == TCPState.ESTABLISHED
    assert server.state == TCPState.SYN_RECEIVED
    assert ack.flags == TCPFlags.ACK
