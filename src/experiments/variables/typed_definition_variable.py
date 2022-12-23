from typing import Dict, Any

from experiments.variables.definition_variable import DefinitionVariable
from experiments.variables.variable import Variable


class TypedDefinitionVariable(DefinitionVariable):
    OBJECT_TYPE_KEY = "objectType"

    def __init__(self, value: Dict[str, Any]):
        """
        A variable used to instantiate objects of the given type
        :param value: a definition of the object and its type defined using OBJECT_TYPE_KEY
        """
        if TypedDefinitionVariable.OBJECT_TYPE_KEY not in value:
            raise KeyError("Please specify object type using the key %s" % TypedDefinitionVariable.OBJECT_TYPE_KEY)
        object_type = value.pop(TypedDefinitionVariable.OBJECT_TYPE_KEY)
        self.object_type = object_type.value if isinstance(object_type, Variable) else object_type
        super().__init__(value)

    def __repr__(self) -> str:
        CLOSE_BRACKET = "}"
        repr_ = super().__repr__()
        parts = [part for part in repr_.split(CLOSE_BRACKET) if len(part) > 0]
        parts.append("%s: %s" % (TypedDefinitionVariable.OBJECT_TYPE_KEY, self.object_type) + CLOSE_BRACKET)
        join_sym = "" if len(parts[0]) <= 1 else ", "
        return join_sym.join(parts)
