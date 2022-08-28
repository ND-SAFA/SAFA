from enum import IntEnum, Enum


class Status(IntEnum):
    SUCCESS = 0
    NOT_STARTED = 1
    IN_PROGRESS = 2
    FAILURE = -1
