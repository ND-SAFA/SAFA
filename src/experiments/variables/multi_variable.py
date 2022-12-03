from typing import List, Any

from experiments.variables.variable import Variable


class MultiVariable(Variable):

    def __init__(self, values: List[Any]):
        super().__init__(values)
