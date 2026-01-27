"""TCP/IP Packets"""

import struct
from enum import IntFlag
from pydantic import BaseModel, Field

HEADER_FMT = "!HHIIBB"
HEADERS_SIZE = struct.calcsize(HEADER_FMT)


class TCPFlags(IntFlag):
    """TCPFlags class"""
    FIN = 0x01
    SYN = 0x02
    ACK = 0x04

class TCPSegment(BaseModel):
    """TCPSegment class"""
    src_port: int = Field(ge=0, le=65535)
    dst_port: int = Field(ge=0, le=65535)
    seq: int
    ack: int
    flags: TCPFlags
    payload: bytes = b""

    def serialize(self) -> bytes:
        """Serialize method"""
        header = struct.pack(
            HEADER_FMT,
            self.src_port,
            self.dst_port,
            self.seq,
            self.ack,
            self.flags,
            0, # reserved
        )
        return header + self.payload

    @classmethod
    def deserialize(cls, raw: bytes) -> "TCPSegment":
        """Deserialize method"""
        header = raw[:HEADERS_SIZE]
        payload = raw[HEADERS_SIZE:]
        src, dst, seq, ack, flags, _ = struct.unpack(HEADER_FMT, header)
        return cls(
            src_port=src,
            dst_port=dst,
            seq=seq,
            ack=ack,
            flags=TCPFlags(flags),
            payload=payload,
        )
