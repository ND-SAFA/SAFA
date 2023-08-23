from enum import Enum, auto


class CeleryStatus(Enum):
    """
    The status of a job.
    """
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILURE = auto()
    REVOKED = auto()
    UNKNOWN = auto()
