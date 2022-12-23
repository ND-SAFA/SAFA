from typing import Dict

from rest_framework import serializers

from experiments.variables.definition_variable import DefinitionVariable
from experiments.variables.experimental_variable import ExperimentalVariable
from experiments.variables.variable import Variable
from server.serializers.serializer_utility import SerializerUtility


class ExperimentSerializer(serializers.Serializer):
    experiment = serializers.DictField(required=True)

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
        if "experiment" in validated_data:
            validated_data = validated_data["experiment"]
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
            if value.get(ExperimentalVariable.SYMBOL, None):
                values = value[ExperimentalVariable.SYMBOL]
                return ExperimentalVariable(values)
            else:
                value_definition = self.create(value)
                return DefinitionVariable(value_definition)
        else:
            return Variable(value)
