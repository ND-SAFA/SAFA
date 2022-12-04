from typing import List, Any

from experiments.variables.variable import Variable


class MultiVariable(Variable, list):

    def __init__(self, values: List[Any]):
        Variable.__init__(self, values)
        list.__init__(self, values)
