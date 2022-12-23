from typing import Dict, Any

from experiments.variables.variable import Variable
from util.uncased_dict import UncasedDict


class DefinitionVariable(UncasedDict, Variable):

    TYPE = "type"  # TODO where should this go??

    def __init__(self, value: Dict[str, Variable]):
        Variable.__init__(self, value=value)
        UncasedDict.__init__(self, dict_=value)
