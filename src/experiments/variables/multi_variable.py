from typing import List, Any

from experiments.variables.variable import Variable


class MultiVariable(Variable, list):
    SYMBOL = "*"

    def __init__(self, values: List[Variable]):
        """
        A variable that contains a list of definitions for obj creation.
        :param values: a list of definitions to create a list of objects from
        """
        Variable.__init__(self, values)
        list.__init__(self, values)

    def get_values_of_all_variables(self) -> List[Any]:
        """
        Gets the value of all variables
        :return: the list of values
        """
        values = []
        for var in self.value:
            values.append(var.value)
        return values
