from typing import Any, List

from experiments.variables.variable import Variable


class ExperimentalVariable(Variable, list):
    SYMBOL = "*"

    def __init__(self, values: List[Variable]):
        """
        A list of Variables to use in experiments
        :param values: a list of variables for experimenting
        """
        Variable.__init__(self, values)
        list.__init__(self, values)
