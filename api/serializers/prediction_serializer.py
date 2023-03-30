from typing import Dict

from rest_framework import serializers

from api.serializers.serializer_utility import SerializerUtility
from tgen.src.variables.variable import Variable


class PredictionSerializer(serializers.Serializer):
    """
    Serializes prediction payload.
    """
    KEY = "definition"
    model = serializers.CharField(max_length=512)
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
        data = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        return data
