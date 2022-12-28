from typing import List, Dict, Any

from util.variables.multi_variable import MultiVariable
from util.variables.variable import Variable


class ExperimentalVariable(MultiVariable):

    def __init__(self, values: List[Any], experimental_param_name_to_val: List[Dict] = None):
        """
        A list of Variables to use in experiments
        :param values: a list of variables for experimenting
        """
        if len(values) > 0 and not isinstance(values[0], Variable):
            values = MultiVariable.from_list(values).value
        self.experimental_param_names_to_vals = experimental_param_name_to_val
        super().__init__(values)
