"""TCP/IP Packets"""
from pydantic import BaseModel, Field

class TCPSegment(BaseModel):
    """TCPSegment class"""
    src_port: int = Field(ge=0, le=65535)
    dst_port: int = Field(ge=0, le=65535)
    seq: int
    ack: int
    payload: bytes = b""

    def serialize(self) -> bytes:
        """Serialize method"""
        return self.model_dump_json().encode()

    @classmethod
    def deserialize(cls, raw: bytes) -> "TCPSegment":
        """Deserialize method"""
        return cls.model_validate_json(raw)
