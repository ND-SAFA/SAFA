from typing import Any, List

from experiments.variables.multi_variable import MultiVariable
from experiments.variables.variable import Variable


class ExperimentalVariable(MultiVariable):

    def __init__(self, values: List[Variable]):
        """
        A list of Variables to use in experiments
        :param values: a list of variables for experimenting
        """
        super().__init__(values)
