from typing import Any, Dict, List

from gen_common.infra.experiment.variables.multi_variable import MultiVariable


class ExperimentalVariable(MultiVariable):

    def __init__(self, values: List[Any], experimental_param_name_to_val: List[Dict] = None, using_jobs: bool = False):
        """
        A list of Variables to use in experiments
        :param values: a list of variables for experimenting
        :param experimental_param_name_to_val: Dictionary of experimental vars per value.
        :param using_jobs: If using jobs will extract experimental params.
        """
        self.experimental_param2val = experimental_param_name_to_val
        if using_jobs:
            self.experimental_param2val = self.__extract_experimental_params(values)
        super().__init__(values)

    @staticmethod
    def __extract_experimental_params(jobs: List["AbstractJob"]) -> List[Dict]:
        """
        Extract experimental params for each job.
        :param jobs: The jobs whose experimental vars are returned.
        :return: ExperimentalVars per job.
        """
        return list(map(lambda j: j.result.experimental_vars, jobs))
