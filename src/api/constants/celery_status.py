from enum import auto

from tgen.common.util.supported_enum import SupportedEnum


class CeleryStatus(SupportedEnum):
    """
    The status of a job.
    """
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILURE = auto()
    REVOKED = auto()
    UNKNOWN = auto()
