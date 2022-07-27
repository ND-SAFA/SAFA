from enum import IntEnum
from typing import Dict


# TODO - placeholder as I am unsure what would be most helpful or how to best status a job (this is currently not being set to anything but success)
class Status(IntEnum):
    SUCCESS = 0
    FAILURE = -1


class JobResult:

    def __init__(self, output: Dict = None, status: Status = Status.SUCCESS):
        """
        Represents the results of a job
        :param output: output of job
        :param status: status of job
        """
        self.output = output
        self.status = status
