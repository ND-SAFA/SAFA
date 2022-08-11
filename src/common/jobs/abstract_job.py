from abc import abstractmethod

from common.jobs.arg_builder import ArgBuilder
from common.jobs.job_result import JobResult


class AbstractJob:

    def __init__(self, arg_builder: ArgBuilder):
        """
        Base job class
        :param arg_builder: job arguments
        """
        self.args = arg_builder.build()

    @abstractmethod
    def __start(self) -> JobResult:
        """
        Runs the logic of the specific job
        :return: result of the job
        """
        pass

    def start(self) -> JobResult:
        """
        Starts the job
        :return: result of the job
        """
        return self.__start()
