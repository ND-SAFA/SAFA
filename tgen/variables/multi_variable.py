from typing import Any, List

from tgen.variables.variable import Variable


class MultiVariable(Variable, list):
    SYMBOL = "*"
    CONCAT = "+"

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

    @staticmethod
    def from_list(orig_list: List) -> "MultiVariable":
        """
        Constructs a multi variable from a list of objects
        :param orig_list: the original list
        :return: the multivariable constructed from the original list
        """
        return MultiVariable([Variable(i) for i in orig_list])
