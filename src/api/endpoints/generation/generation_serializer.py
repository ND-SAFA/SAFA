from typing import Dict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.utils.serializer_utility import SerializerUtility
from tgen.variables.variable import Variable


class GenerationSerializer(AbstractSerializer):
    """
    Serialized the generation payload
    """
    model = serializers.CharField(max_length=512)
    prompt = serializers.CharField(max_length=512, trim_whitespace=False)

    def create(self, validated_data: Dict) -> Dict[str, Variable]:
        """
        Creates experiment instructions by converting Dict of primitives into
        one of variables.
        :param validated_data: Dictionary composed of primitive values.
        :return: Mapping between keys and variables.
        """
        data = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        return data
