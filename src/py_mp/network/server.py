import socket as _sock
from py_mp.models import ClientBaseModel as _ClientBase
from py_mp.commands import ClientCommand as _ClientCommand, ServerCommand as _ServerCommand, BaseCommand as _BaseCommand, ServerSideClientCommand as _ServerSideClientCommand, ServerSideServerCommand as _ServerSideServerCommand


class NetworkServerBase:
    def __init__(self, host: str | None = None, port: int | None = None, auto_bind: bool = True) -> None:
        """
        Initializes all the variables in the class and prepares them for use.

        Parameters
        ----------
            host: str | None, by default None
                Specify the hostname of the server to bind to
            port: int | None, by default None
                Specify the port to bind to
            auto_bind: bool, by default True
                Automatically bind the socket to a port and host
        """
        self.conn: _sock.socket = _sock.socket(_sock.AF_INET, _sock.SOCK_STREAM)
        self._binded: bool = False
        self.addr: tuple[str, int] | None = None
        self.clients: list[_ClientBase] = []

        # Auto-bind
        if auto_bind:
            if host and port:
                self.bind(host, port)

    def __repr__(self) -> str:
        return f"<NetworkServerBase {f'binded ({self.addr[0]}:{self.addr[1]})' if self.is_binded() else 'not binded'}>"

    def bind(self,  host: str, port: int) -> _sock.socket:
        """Bind the socket to a host and port

        Parameters
        ----------
        host : str
            The Hostname or IP address to bind the server to
        port : int
            The Port to bind the server to

        Returns
        -------
        socket.socket
            The socket object that is binded to the given host and port
        """
        self.addr = (host, port)
        self.conn.bind(self.addr)
        self._binded = True
        return self.conn

    def _accept(self, amount: int = 1) -> None:
        """Wrapper of the socket.accept() method including a check if the socket is binded to a host and port

        Parameters
        ----------
        amount : int, by default 1
            The amount of clients to accept

        Raises
        ------
        ConnectionError
            The socket is not binded to a host and port
        """
        if not self.is_binded():
            raise ConnectionError("Not binded to any addr")
        self.conn.listen(amount)
        while len(self.clients) < amount:
            self.clients.append(_ClientBase.from_accept(*self.conn.accept()))

    def _recv(self, size: int, client: _ClientBase) -> bytes:
        """Wrapper of the socket.recv() method including a check if the socket is binded to a host and port

        Parameters
        ----------
        size : int
            The amount of bytes to receive
        client : ClientBase
            The client to receive the data from

        Returns
        -------
        bytes
            The received bytes

        Raises
        ------
        ConnectionError
            The socket is not binded to a host and port
        """
        if not self.is_binded():
            raise ConnectionError("Not binded to any addr")
        if client not in self.clients:
            raise ConnectionError("Client not connected")
        return client.conn.recv(size)

    def _send(self, data: bytes, client: _ClientBase) -> None:
        """Wrapper of the socket.send() method including a check if the socket is binded to a host and port

        Parameters
        ----------
        data : bytes
            The data to send to the client
        client : ClientBase
            The client to send the data to

        Raises
        ------
        ConnectionError
            The socket is not binded to a host and port
        """
        if not self.is_binded():
            raise ConnectionError("Not binded to any addr")
        if client not in self.clients:
            raise ConnectionError("Client not connected")
        client.conn.send(data)

    def is_binded(self) -> bool:
        """Check if the socket is binded to a host and port

        Returns
        -------
        bool
            True if the socket is binded to a host and port, False if not
        """
        return self._binded


class NetworkServer(NetworkServerBase):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes all the variables in the class and prepares them for use.

        The difference between this class and the NetworkServerBase class is that this class
        automatically sends the length of the data to the client and then sends the data
        """
        self.ENCODING: str = "utf-8"
        super().__init__(*args, **kwargs)

    def accept(self, amount: int = 1) -> None:
        """Accept a client

        Parameters
        ----------
        amount : int, by default 1
            The amount of clients to accept
        """
        self._accept(amount)

    def send(self, data: str, client: _ClientBase) -> None:
        """Send data to a specific client

        Parameters
        ----------
        data : bytes
            The data to send to the client
        client : ClientBase
            The client to send the data to
        """
        if client not in self.clients:
            raise ConnectionError("Client not connected")
        data = data.encode(self.ENCODING)
        length = len(data)
        self._send(length.to_bytes(8, "big"), client)
        if int.from_bytes(self._recv(8, client), "big") == length:
            self._send(data, client)

    def send_to(self, data: str, *clients: _ClientBase) -> None:
        """Send data to several clients

        Parameters
        ----------
        data : str
            The data to send to the client
        clients : list[ClientBase]
            The clients to send the data to
        """
        for client in clients:
            self.send(data, client)

    def send_all(self, data: str) -> None:
        """Send data to all clients

        Parameters
        ----------
        data : str
            The data to send to the client
        """
        for client in self.clients:
            self.send(data, client)

    def recv(self, client: _ClientBase) -> str:
        """Receive data from a specific client

        Parameters
        ----------
        client : ClientBase
            The client to receive the data from

        Returns
        -------
        str
            The received data
        """
        if client not in self.clients:
            raise ConnectionError("Client not connected")

        length = int.from_bytes(self._recv(8, client), "big")
        self._send(length.to_bytes(8, "big"), client)
        return self._recv(length, client).decode(self.ENCODING)


class CommandServer(NetworkServer):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes all the variables in the class and prepares them for use.

        The difference between this class and the NetworkClient class is that this class
        sends and receives data as strings instead of bytes.
        """
        super().__init__(*args, **kwargs)

    def send(self, command: _ServerCommand | _ServerSideServerCommand, client: _ClientBase) -> None:
        """Send data to the server

        Parameters
        ----------
        command : ClientCommand | ServerCommand
            The command to send to the server
        client : ClientBase
            The client to send the data to
        """
        if isinstance(command, _ServerSideServerCommand):
            command = command.to_client_cmd()
        super().send(command.serialize(), client)

    def send_to(self, command: _ServerCommand | _ServerSideServerCommand, *clients: _ClientBase) -> None:
        """Send data to several clients

        Parameters
        ----------
        command : ServerCommand | ServerSideServerCommand
            The data to send to the client
        clients : list[ClientBase]
            The clients to send the data to
        """
        for client in clients:
            self.send(command, client)

    def send_all(self, command: _ServerCommand | _ServerSideServerCommand) -> None:
        """Send data to all clients

        Parameters
        ----------
        command : ClientCommand | ServerCommand
            The command to send to the server
        """
        if isinstance(command, _ServerSideServerCommand):
            command = command.to_client_cmd()
        super().send_all(command.serialize())

    def recv(self, client: _ClientBase) -> _ServerSideClientCommand:
        """Receive data from the server

        Parameters
        ----------
        client : ClientBase
            The client to receive the data from

        Returns
        -------
        str
            The received data
        """
        return _ServerSideClientCommand.from_client_cmd(_BaseCommand.deserialize(super().recv(client)), client)


if __name__ == '__main__':
    from py_mp.commands import ServerSideServerCommand, NetworkFlag

    server = CommandServer("localhost", 1234)
    server.accept(2)

    print(server.recv(server.clients[0]))
    print(server.recv(server.clients[1]))
    server.send(ServerSideServerCommand(NetworkFlag.CONNECTED, server.clients[0]), server.clients[0])
    server.send(ServerSideServerCommand(NetworkFlag.CONNECTED, server.clients[1]), server.clients[1])
