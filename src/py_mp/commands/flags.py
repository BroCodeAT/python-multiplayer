from enum import IntFlag as _IntFlag


class CommandFlag(_IntFlag):
    pass


class NetworkFlag(CommandFlag):
    """
    Flags for the Network Commands
    Reserved Flags: 100 - 199
    """
    DISCONNECTED = 100
    CONNECTED = 101
