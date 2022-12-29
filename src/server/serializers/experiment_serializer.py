from typing import Dict

from rest_framework import serializers

from server.serializers.serializer_utility import SerializerUtility
from util.variables.definition_variable import DefinitionVariable
from util.variables.experimental_variable import ExperimentalVariable
from util.variables.multi_variable import MultiVariable
from util.variables.typed_definition_variable import TypedDefinitionVariable
from util.variables.variable import Variable


class ExperimentSerializer(serializers.Serializer):
    KEY = "definition"
    definition = serializers.DictField(required=True)

    def update(self, instance, validated_data):
        SerializerUtility.update_error()

    def create(self, validated_data: Dict) -> Dict[str, Variable]:
        """
        Creates experiment instructions by converting Dict of primitives into
        one of variables.
        :param validated_data: Dictionary composed of primitive values.
        :return: Mapping between keys and variables.
        """
        result: Dict[str, Variable] = {}
        if self.KEY in validated_data:
            validated_data = validated_data[self.KEY]
        for key, value in validated_data.items():
            result[key] = self.create_variable(value)
        return result

    def create_variable(self, value):
        """
        Creates variable from primitive, dict, or list.
        :param value: The value to convert into a variable.
        :return: Variable encapsulating value.
        """
        if isinstance(value, dict):
            value_definition = self.create(value)
            if value.get(ExperimentalVariable.SYMBOL, None):
                values = value[ExperimentalVariable.SYMBOL]
                return ExperimentalVariable(values)
            elif value.get(TypedDefinitionVariable.OBJECT_TYPE_KEY, None):
                return TypedDefinitionVariable(value_definition)
            else:
                return DefinitionVariable(value_definition)
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], Dict):
            values = [self.create_variable(v) for v in value]
            return MultiVariable(values)
        else:
            return Variable(value)
