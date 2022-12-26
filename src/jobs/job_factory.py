from typing import Type, Union

from util.variables.definition_variable import DefinitionVariable
from jobs.abstract_job import AbstractJob


class JobFactory:

    def __init__(self, job_definition: Union[str, DefinitionVariable]):
        """
        Responsible for creating jobs
        :param job_definition: all necessary parameters for creating the job (may be json or definition var)
        """
        if not isinstance(job_definition, DefinitionVariable):
            # TODO @alberto please add serializing to this
            pass
        self.job_definition = job_definition

    def build(self, job_class: Type[AbstractJob]) -> AbstractJob:
        """
        Creates job using the job definition
        :param job_class: the class of job to build
        :return: Job
        """
        return job_class.initialize_from_definition(self.job_definition)
