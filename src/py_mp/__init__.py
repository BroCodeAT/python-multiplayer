"""
The py_mp package is a simple python module for creating a client-server network
application. It is designed to be used for games and other applications that
require a client-server architecture.

The package provides multiple ways to communicate between the client and server.
"""

from .network import NetworkServer, NetworkClient, CommandClient, CommandServer
from .commands import ClientCommand, ServerCommand, ServerSideClientCommand, ServerSideServerCommand

__version__ = "0.1.2"
