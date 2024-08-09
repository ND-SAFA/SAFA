from typing import Dict

from common_resources.tools.util.uncased_dict import UncasedDict
from common_resources.tools.variables.variable import Variable


class DefinitionVariable(UncasedDict, Variable):

    def __init__(self, value: Dict[str, Variable]):
        """
        A variable that contains an object definition and can be used to instantiate the object
        :param value: a dictionary mapping parameter name to a variable containing the parameter value
        """
        Variable.__init__(self, value=value)
        UncasedDict.__init__(self, dict_=value)
