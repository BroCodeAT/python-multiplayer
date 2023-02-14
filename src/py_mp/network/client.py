import socket as _sock
from py_mp.commands import ClientCommand as _ClientCommand, \
    ServerCommand as _ServerCommand, BaseCommand as _BaseCommand


class NetworkClientBase:
    def __init__(self, host: str | None = None, port: int | None = None, auto_connect: bool = True) -> None:
        """
        Initializes all the variables in the class and prepares them for use.

        Parameters
        ----------
            host: str | None, by default None
                Specify the hostname of the server to connect to
            port: int | None, by default None
                Specify the port to connect to
            auto_connect: bool, by default True
                Automatically connect the socket to a port and host
        """
        self.conn: _sock.socket = _sock.socket(_sock.AF_INET, _sock.SOCK_STREAM)
        self._connected: bool = False
        self.addr: tuple[str, int] | None = None

        if auto_connect:
            if host and port:
                self.connect(host, port)

    def __repr__(self) -> str:
        return f"<NetworkClientBase " \
               f"{f'connected ({self.addr[0]}:{self.addr[1]})' if self.is_connected() else 'not connected'}>"

    def connect(self,  host: str, port: int):
        """Connect the socket to a host and port

        Parameters
        ----------
        host : str
            The Hostname or IP address of the server to connect to
        port : int
            The Port of the server to connect to

        Returns
        -------
        socket.socket
            The socket object that is connected to the given host and port
        """
        self.addr = (host, port)
        self.conn.connect(self.addr)
        self._connected = True

    def _recv(self, size: int) -> bytes:
        """Wrapper of the socket.recv() method including a check if the socket is connected to a host and port

        Parameters
        ----------
        size : int
            The amount of bytes to receive

        Returns
        -------
        bytes
            The received bytes

        Raises
        ------
        ConnectionError
            The socket is not connected to a host and port
        """
        if self.is_connected():
            return self.conn.recv(size)
        else:
            raise ConnectionError("Not connected to any server")

    def _send(self, data: bytes):
        """Wrapper of the socket.send() method including a check if the socket is connected to a host and port

        Parameters
        ----------
        data : bytes
            The data to send to the server

        Raises
        ------
        ConnectionError
            The socket is not connected to a host and port
        """
        if self.is_connected():
            self.conn.send(data)
        else:
            raise ConnectionError("Not connected to any server")

    def is_connected(self) -> bool:
        """Check if the socket is connected to a host and port (server)

        Returns
        -------
        bool
            True if the socket is connected to a host and port, False if not
        """
        return self._connected


class NetworkClient(NetworkClientBase):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes all the variables in the class and prepares them for use.

        The difference between this class and the NetworkClientBase class is that this class
        first sends the size of the data to the server before sending the data itself.
        """
        self.ENCODING: str = "utf-8"
        super().__init__(*args, **kwargs)

    def send(self, data: str):
        """Send data to the server

        Parameters
        ----------
        data : bytes
            The data to send to the server
        """
        data = data.encode(self.ENCODING)
        length = len(data)
        self._send(length.to_bytes(8, "big"))
        if int.from_bytes(self._recv(8), "big") == length:
            self._send(data)

    def recv(self) -> str:
        """Receive data from the server

        Returns
        -------
        str
            The received data
        """
        length = int.from_bytes(self._recv(8), "big")
        self._send(length.to_bytes(8, "big"))
        return self._recv(length).decode(self.ENCODING)


class CommandClient(NetworkClient):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes all the variables in the class and prepares them for use.

        The difference between this class and the NetworkClient class is that this class
        sends and receives data as strings instead of bytes.
        """
        super().__init__(*args, **kwargs)

    def send(self, command: _ClientCommand | _ServerCommand):
        """Send data to the server

        Parameters
        ----------
        command : ClientCommand | ServerCommand
            The command to send to the server
        """
        super().send(command.serialize())

    def recv(self) -> _BaseCommand:
        """Receive data from the server

        Returns
        -------
        str
            The received data
        """
        return _BaseCommand.deserialize(super().recv())
