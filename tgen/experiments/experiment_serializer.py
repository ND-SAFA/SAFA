from typing import Dict

from tgen.variables.definition_variable import DefinitionVariable
from tgen.variables.experimental_variable import ExperimentalVariable
from tgen.variables.multi_variable import MultiVariable
from tgen.variables.typed_definition_variable import TypedDefinitionVariable
from tgen.variables.undetermined_variable import UndeterminedVariable
from tgen.variables.variable import Variable


class ExperimentSerializer:
    KEY = "definition"

    @staticmethod
    def create(validated_data: Dict) -> Dict[str, Variable]:
        """
        Creates experiment instructions by converting Dict of primitives into
        one of variables.
        :param validated_data: Dictionary composed of primitive values.
        :return: Mapping between keys and variables.
        """
        result: Dict[str, Variable] = {}
        if ExperimentSerializer.KEY in validated_data:
            validated_data = validated_data[ExperimentSerializer.KEY]
        for key, value in validated_data.items():
            result[key] = ExperimentSerializer.create_variable(value)
        return result

    @staticmethod
    def create_variable(value):
        """
        Creates variable from primitive, dict, or list.
        :param value: The value to convert into a variable.
        :return: Variable encapsulating value.
        """
        if isinstance(value, dict):
            value_definition = ExperimentSerializer.create(value)
            if value.get(ExperimentalVariable.SYMBOL, None):
                values = [ExperimentSerializer.create_variable(v) for v in value[ExperimentalVariable.SYMBOL]]
                return ExperimentalVariable(values)
            elif value.get(TypedDefinitionVariable.OBJECT_TYPE_KEY, None):
                return TypedDefinitionVariable(value_definition)
            else:
                return DefinitionVariable(value_definition)
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], Dict):
            values = [ExperimentSerializer.create_variable(v) for v in value]
            return MultiVariable(values)
        else:
            if isinstance(value, str) and value.strip() == UndeterminedVariable.SYMBOL:
                return UndeterminedVariable()
            return Variable(value)
