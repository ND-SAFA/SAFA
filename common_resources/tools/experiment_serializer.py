import os
from typing import Dict

from common_resources.tools.variables.definition_variable import DefinitionVariable
from common_resources.tools.variables.experimental_variable import ExperimentalVariable
from common_resources.tools.variables.multi_variable import MultiVariable
from common_resources.tools.variables.typed_definition_variable import TypedDefinitionVariable
from common_resources.tools.variables.undetermined_variable import UndeterminedVariable
from common_resources.tools.variables.variable import Variable


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
                experiment_vals = value[ExperimentalVariable.SYMBOL]
                if isinstance(experiment_vals, dict) and ExperimentalVariable.CONCAT in experiment_vals:
                    base_val, concat_values = experiment_vals[ExperimentalVariable.CONCAT]
                    experiment_vals = [os.path.join(base_val, v) for v in concat_values]
                values = [ExperimentSerializer.create_variable(v) for v in experiment_vals]
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
