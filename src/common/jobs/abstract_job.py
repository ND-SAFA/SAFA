from abc import abstractmethod

from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.jobs.job_result import JobResult


class AbstractJob:

    def __init__(self, arg_builder: AbstractArgsBuilder):
        """
        Base job class
        :param arg_builder: job arguments
        """
        self.args = arg_builder.build()

    @abstractmethod
    def start(self) -> JobResult:
        """
        Runs the logic of the specific job
        :return: result of the job
        """
        pass


