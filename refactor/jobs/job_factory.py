from jobs.abstract_job import AbstractJob


class JobFactory:
    def __init__(self):
        """
        Storage of job arguments and creator of jobs.
        """
        raise NotImplementedError()

    def build(self) -> AbstractJob:
        """
        Creates job using job argument and any additional parameters.
        :return: Job
        :rtype:
        """
        raise NotImplementedError()
