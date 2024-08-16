from enum import IntEnum


class Status(IntEnum):
    SUCCESS = 0
    NOT_STARTED = 1
    IN_PROGRESS = 2
    FAILURE = -1
    UNKNOWN = -2
