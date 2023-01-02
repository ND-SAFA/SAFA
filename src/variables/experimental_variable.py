from typing import Any, Dict, List

from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult
from variables.multi_variable import MultiVariable
from variables.variable import Variable


class ExperimentalVariable(MultiVariable):

    def __init__(self, values: List[Any], experimental_param_name_to_val: List[Dict] = None):
        """
        A list of Variables to use in experiments
        :param values: a list of variables for experimenting
        :param experimental_param_name_to_val: Dictionary of experimental vars per value.
        """
        if len(values) > 0 and not isinstance(values[0], Variable):
            values = MultiVariable.from_list(values).value
        if len(values) > 0 and isinstance(values[0], AbstractJob):
            self.experimental_param_names_to_vals = self.__extract_experimental_params(values)
        else:
            self.experimental_param_names_to_vals = experimental_param_name_to_val
        super().__init__(values)

    @staticmethod
    def __extract_experimental_params(jobs: List[Any]) -> List[Dict]:
        """
        Extract experimental params for each job.
        :param jobs: The jobs whose experimental vars are returned.
        :return: ExperimentalVars per job.
        """
        return list(map(lambda j: j.result[JobResult.EXPERIMENTAL_VARS], jobs))
