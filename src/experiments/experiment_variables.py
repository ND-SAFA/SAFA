import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Type, Tuple, Union, Any
from jobs.abstract_job import AbstractJob
from train.metrics.supported_trace_metric import SupportedTraceMetric


@dataclass
class ExperimentVariables:
    """
    The type of job (e.g. Predict/Train)
    """
    job_type: Type[AbstractJob]
    """
    A dictionary containing name, value mappings for all constant variables
    """
    constant: Dict[str, Any] = field(default_factory=dict)
    """
    A dictionary containing name, list of possible value mappings for all experimental variables
    """
    experimental: Dict[str, List] = field(default_factory=dict)
    """
    A list containing name of all variables whose values will come from the best job of a previous step
    """
    best_from_previous: List[str] = field(default_factory=list)
    """
    An optional tuple containing the metric to use to determine the best job and a bool that if True will aim to maximize the metric 
    else minimize it
    """
    comparison_info: Tuple[Union[str, SupportedTraceMetric], bool] = None
    """
    Initialized post init to determine all different combinations of the experimental vars
    """
    all_experimental_combinations: List[Dict] = field(init=False)

    def __post_init__(self):
        self.all_experimental_combinations = self._get_all_combinations_of_experimental_vars()

    def _get_all_combinations_of_experimental_vars(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all possible combinations of experimental variables
        :return: a list of all possible combinations of experimental variables
        """
        var_names = list(self.experimental.keys())
        experimental_var_combinations = list(itertools.product(*[self.experimental[name] for name in var_names]))
        return [{var_names[i]: experimental_vars[i] for i in range(len(var_names))}
                for experimental_vars in experimental_var_combinations]
