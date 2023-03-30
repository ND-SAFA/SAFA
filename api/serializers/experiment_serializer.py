from typing import Dict

from rest_framework import serializers

from api.serializers.serializer_utility import SerializerUtility
from tgen.src.experiments.experiment import Experiment
from tgen.src.util.object_creator import ObjectCreator
from tgen.src.variables.variable import Variable


class ExperimentSerializer(serializers.Serializer):
    """
    Creates experiment from experiment definition.
    """
    KEY = "definition"
    definition = serializers.DictField(required=True)

    def update(self, instance, validated_data):
        """
        Not implemented. Throws error if called.
        """
        SerializerUtility.update_error()

    def create(self, validated_data: Dict) -> Dict[str, Variable]:
        """
        Creates experiment instructions by converting Dict of primitives into
        one of variables.
        :param validated_data: Dictionary composed of primitive values.
        :return: Mapping between keys and variables.
        """
        if self.KEY not in validated_data:
            raise Exception(f"Expected data to contain key: {self.KEY}")
        validated_data = validated_data[self.KEY]
        experiment = ObjectCreator.create(Experiment, override=True, **validated_data)
        return experiment
