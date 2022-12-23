from typing import Any, List

from experiments.variables.definition_variable import DefinitionVariable
from experiments.variables.variable import Variable


class MultiVariable(Variable, list):
    SYMBOL = "*"

    def __init__(self, values: List[DefinitionVariable]):
        """
        A variable that contains a list of definitions for object creation.
        :param values: a list of definitions to create a list of objects from
        """
        Variable.__init__(self, values)
        list.__init__(self, values)
