# Python Multiplayer

<a href="https://pypi.org/project/python-multiplayer/"><img src="https://badge.fury.io/py/python-multiplayer.png" alt="PyPI version" height="18"></a>

Framework for Client Server Structure in Python.
Is intended to be used for multiplayer games in pygame with this Module.

[pygame-multiplayer](https://github.com/BroCodeAT/python-multiplayer)

----

## Planned features
- [x] Command based Network
- [ ] Threaded Network
- [ ] Async Network


## Installation

```bash
pip install python-multiplayer
```

## Usage (Command Server/Client)

Server:
```python
from py_mp import CommandServer
from py_mp import ServerSideServerCommand
from py_mp.commands import NetworkFlag

server = CommandServer("localhost", 5000)
server.accept()

# Receive a Command from the Client
com = server.recv(server.clients[0])
print(com)

# Send a Test Command back to the Client
server.send(
    ServerSideServerCommand(NetworkFlag.CONNECTED, server.clients[0], test="test"), 
    server.clients[0]
)
```
Client:
```python
from py_mp import CommandClient
from py_mp import ClientCommand
from py_mp.commands import NetworkFlag

client = CommandClient("localhost", 5000)

# Send a Test Command to the Server
client.send(ClientCommand(NetworkFlag.CONNECTED, test="test"))

# Receive a Command from the Server
com = client.recv()
print(com)
```
