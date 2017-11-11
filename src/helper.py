import enum

class State(enum.IntEnum):
    NOT_CONNECTED = 0
    NEGOTIATING = 1
    CONNECTED = 2