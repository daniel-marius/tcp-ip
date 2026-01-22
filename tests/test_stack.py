"""Test TCP/IP stack"""

from tcp_ip.simulation.node import build_stack

def test_full_stack_roundtrip() -> None:
    app = build_stack()

    wire_data = app.send_message("hello")
    received = app.receive_message(wire_data)

    assert received == '{"src_port":1234,"dst_port":80,"seq":1,"ack":0,"payload":"hello"}'
