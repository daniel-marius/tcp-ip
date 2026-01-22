"""TCP/IP Layer Interface"""

from abc import ABC, abstractmethod

class Layer(ABC):
    """Abstract class Layer"""

    @abstractmethod
    def send(self, data: bytes) -> bytes:
        """Abstract method send"""

    @abstractmethod
    def receive(self, data: bytes) -> bytes:
        """Abstract method receive"""
