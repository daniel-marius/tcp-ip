"""Application Layer"""

from tcp_ip.core.interfaces import Layer

class ApplicationLayer:
    """Application Layer class"""

    def __init__(self, transport: Layer) -> None:
        self._transport = transport

    def send_message(self, msg: str) -> bytes:
        """Send method"""
        return self._transport.send(msg.encode())

    def receive_message(self, raw: bytes) -> str:
        """Receive method"""
        return raw.decode()
