from typing import Dict, Any

from experiments.variables.definition_variable import DefinitionVariable
from experiments.variables.variable import Variable
from util.uncased_dict import UncasedDict


class TypedVariable(DefinitionVariable):
    OBJECT_TYPE_KEY = "objectType"

    def __init__(self, value: Dict[str, Variable]):
        """
        A variable used to instantiate objects of the given type
        :param value: a definition of the object and its type defined using OBJECT_TYPE_KEY
        """
        if TypedVariable.OBJECT_TYPE_KEY not in value:
            raise KeyError("Please specify object type using the key %s" % TypedVariable.OBJECT_TYPE_KEY)
        self.object_type = value.pop(TypedVariable.OBJECT_TYPE_KEY)
        Variable.__init__(self, value=value)
        UncasedDict.__init__(self, dict_=value)
