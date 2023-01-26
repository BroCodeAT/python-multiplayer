from dataclasses import dataclass as _dc
import socket as _sock


@_dc
class ClientBase:
    conn: _sock.socket
    address: str
    port: int

    @classmethod
    def from_accept(cls, conn: _sock.socket, addr: tuple[str, int]):
        return cls(conn, addr[0], addr[1])
